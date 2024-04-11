import base64
import time
import urllib.parse
from typing import List, Optional

import requests
from requests import Session, Response
from requests.auth import AuthBase

from .access_token import AccessToken
from .credentials import HttpBasic, HttpBearer, ApiKey, OAuth2, Anonymous, CredentialsInterface
from .exceptions import InvalidAccessTokenException, InvalidCredentialsException
from .token_store import MemoryTokenStore, TokenStoreInterface


class AuthenticatorInterface(AuthBase):
    pass


class AnonymousAuthenticator(AuthenticatorInterface):
    @classmethod
    def __init__(cls, credentials: Anonymous):
        cls.credentials = credentials

    @classmethod
    def __call__(cls, request):
        return request


class HttpBasicAuthenticator(AuthenticatorInterface):
    credentials: HttpBasic = None

    @classmethod
    def __init__(cls, credentials: HttpBasic):
        cls.credentials = credentials

    @classmethod
    def __call__(cls, request):
        basic = base64.b64encode((cls.credentials.username + ":" + cls.credentials.password).encode('utf-8')).decode('ascii')
        request.headers["Authorization"] = "Basic " + basic
        return request


class HttpBearerAuthenticator(AuthenticatorInterface):
    credentials: HttpBearer = None

    @classmethod
    def __init__(cls, credentials: HttpBearer):
        cls.credentials = credentials

    @classmethod
    def __call__(cls, request):
        request.headers["Authorization"] = "Bearer " + cls.credentials.token
        return request


class ApiKeyAuthenticator(AuthenticatorInterface):
    credentials: ApiKey = None

    @classmethod
    def __init__(cls, credentials: ApiKey):
        cls.credentials = credentials

    @classmethod
    def __call__(cls, request):
        request.headers[cls.credentials.name] = cls.credentials.token
        return request


class OAuth2Authenticator(AuthenticatorInterface):
    EXPIRE_THRESHOLD: int = 60 * 10

    credentials: OAuth2 = None
    scopes: Optional[list[str]] = None
    token_store: TokenStoreInterface = None

    @classmethod
    def __init__(cls, credentials: OAuth2):
        cls.credentials = credentials
        cls.scopes = credentials.scopes
        if credentials.token_store:
            cls.token_store = credentials.token_store
        else:
            cls.token_store = MemoryTokenStore()

    @classmethod
    def __call__(cls, request):
        request.headers["Authorization"] = "Bearer " + cls.get_access_token()
        return request

    @classmethod
    def build_redirect_url(cls, redirect_url: str, scopes: List[str], state: str) -> str:
        parameters = {
            "response_type": "code",
            "client_id": cls.credentials.client_id,
        }

        if redirect_url:
            parameters["redirect_uri"] = redirect_url

        if scopes:
            parameters["scope"] = ",".join(scopes)
        elif cls.scopes:
            parameters["scope"] = ",".join(cls.scopes)

        if state:
            parameters["state"] = state

        return cls.credentials.authorization_url + "?" + urllib.parse.urlencode(parameters)

    @classmethod
    def fetch_access_token_by_code(cls, code: str) -> AccessToken:
        credentials = HttpBasic(cls.credentials.client_id, cls.credentials.client_secret)

        headers = {
            "Accept": "application/json",
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
        }

        response = cls.new_http_client(credentials).post(cls.credentials.token_url, headers=headers, data=data)

        return cls.parse_token_response(response)

    @classmethod
    def fetch_access_token_by_client_credentials(cls) -> AccessToken:
        credentials = HttpBasic(cls.credentials.client_id, cls.credentials.client_secret)

        headers = {
            "Accept": "application/json",
        }

        data = {
            "grant_type": "client_credentials",
        }

        if cls.scopes:
            data["scope"] = ",".join(cls.scopes)

        response = cls.new_http_client(credentials).post(cls.credentials.token_url, headers=headers, data=data)

        return cls.parse_token_response(response)

    @classmethod
    def fetch_access_token_by_refresh(cls, refresh_token: str) -> AccessToken:
        credentials = HttpBearer(cls.get_access_token(False, 0))

        headers = {
            "Accept": "application/json",
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        response = cls.new_http_client(credentials).post(cls.credentials.token_url, headers=headers, data=data)

        return cls.parse_token_response(response)

    @classmethod
    def get_access_token(cls, automatic_refresh: bool = True, expire_threshold: int = EXPIRE_THRESHOLD) -> str:
        timestamp = time.time()

        access_token = cls.credentials.token_store.get()
        if not access_token or access_token.get_expires_in_timestamp() < timestamp:
            access_token = cls.fetch_access_token_by_client_credentials()

        if access_token.get_expires_in_timestamp() > (timestamp + expire_threshold):
            return access_token.access_token

        if automatic_refresh and access_token.refresh_token:
            access_token = cls.fetch_access_token_by_refresh(access_token.refresh_token)

        return access_token.access_token

    @classmethod
    def parse_token_response(cls, response: Response) -> AccessToken:
        if response.status_code != 200:
            raise InvalidAccessTokenException(
                "Could not obtain access token, received a non successful status code: " + str(response.status_code))

        token = AccessToken.model_validate_json(json_data=response.content)

        cls.token_store.persist(token)

        return token

    @classmethod
    def new_http_client(cls, credentials: CredentialsInterface) -> Session:
        return HttpClientFactory(AuthenticatorFactory.factory(credentials)).factory()


class AuthenticatorFactory:
    @staticmethod
    def factory(credentials: CredentialsInterface) -> AuthenticatorInterface:
        if isinstance(credentials, HttpBasic):
            return HttpBasicAuthenticator(credentials)
        elif isinstance(credentials, HttpBearer):
            return HttpBearerAuthenticator(credentials)
        elif isinstance(credentials, ApiKey):
            return ApiKeyAuthenticator(credentials)
        elif isinstance(credentials, OAuth2):
            return OAuth2Authenticator(credentials)
        elif isinstance(credentials, Anonymous):
            return AnonymousAuthenticator(credentials)
        else:
            raise InvalidCredentialsException("Could not find authenticator for credentials")


class HttpClientFactory:
    authenticator: AuthenticatorInterface = None

    @classmethod
    def __init__(cls, authenticator: AuthenticatorInterface):
        cls.authenticator = authenticator

    @classmethod
    def factory(cls) -> Session:
        session = requests.Session()
        session.auth = cls.authenticator
        session.headers['User-Agent'] = 'SDKgen Client v1.0'
        session.headers['Accept'] = 'application/json'
        return session

