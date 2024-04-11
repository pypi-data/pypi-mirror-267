from typing import Optional

from .access_token import AccessToken


class TokenStoreInterface:
    @classmethod
    def get(cls) -> AccessToken:
        pass

    @classmethod
    def persist(cls, token: AccessToken):
        pass

    @classmethod
    def remove(cls):
        pass

    pass


class MemoryTokenStore(TokenStoreInterface):
    token: Optional[AccessToken] = None

    @classmethod
    def __init__(cls):
        cls.token = None

    @classmethod
    def get(cls) -> AccessToken:
        return cls.token

    @classmethod
    def persist(cls, token: AccessToken):
        cls.token = token

    @classmethod
    def remove(cls):
        cls.token = None
