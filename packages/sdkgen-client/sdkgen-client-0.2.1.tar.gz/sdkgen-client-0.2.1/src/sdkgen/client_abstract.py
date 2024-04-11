from requests import Session

from .authenticator import AuthenticatorFactory, HttpClientFactory, AuthenticatorInterface
from .credentials import CredentialsInterface
from .parser import Parser


class ClientAbstract:
    USER_AGENT = "SDKgen Client v1.0"

    authenticator: AuthenticatorInterface = None
    http_client: Session = None
    parser: Parser = None

    @classmethod
    def __init__(cls, base_url: str, credentials: CredentialsInterface):
        cls.authenticator = AuthenticatorFactory.factory(credentials)
        cls.http_client = HttpClientFactory(cls.authenticator).factory()
        cls.parser = Parser(base_url)


class TagAbstract:
    http_client: Session = None
    parser: Parser = None

    @classmethod
    def __init__(cls, http_client: Session, parser: Parser):
        cls.http_client = http_client
        cls.parser = parser
