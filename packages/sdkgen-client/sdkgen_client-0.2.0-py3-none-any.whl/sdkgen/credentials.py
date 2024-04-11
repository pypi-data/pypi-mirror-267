from typing import Optional

from .token_store import TokenStoreInterface


class CredentialsInterface:
    pass


class Anonymous(CredentialsInterface):
    pass


class ApiKey(CredentialsInterface):
    token: str = None
    name: str = None
    in_: str = None

    @classmethod
    def __init__(cls, token: str, name: str, in_: str):
        cls.token = token
        cls.name = name
        cls.in_ = in_


class HttpBasic(CredentialsInterface):
    username: str = None
    password: str = None

    @classmethod
    def __init__(cls, username: str, password: str):
        cls.username = username
        cls.password = password


class HttpBearer(CredentialsInterface):
    @classmethod
    def __init__(cls, token: str):
        cls.token = token


class OAuth2(CredentialsInterface):
    client_id: str = None
    client_secret: str = None
    token_url: str = None
    authorization_url: str = None
    token_store: Optional[TokenStoreInterface] = None
    scopes: Optional[list[str]] = None

    @classmethod
    def __init__(cls, client_id: str, client_secret: str, token_url: str, authorization_url: str,
                 token_store: Optional[TokenStoreInterface], scopes: Optional[list[str]]):
        cls.client_id = client_id
        cls.client_secret = client_secret
        cls.token_url = token_url
        cls.authorization_url = authorization_url
        cls.token_store = token_store
        cls.scopes = scopes
