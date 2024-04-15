from abc import abstractmethod, ABC
import os
import requests
from typing import Optional
from requests.exceptions import RequestException

from .user import Principal
from opencredit.db.conn import WithDB
from opencredit.server.models import V1Principal


class KeyProvider(ABC):
    """API key provider"""

    @abstractmethod
    def create_key(self) -> str:
        pass

    @abstractmethod
    def is_key(self, token: str) -> bool:
        pass

    @abstractmethod
    def validate(self, token: str) -> Principal:
        pass


class MockProvider(KeyProvider):
    """Mock key provider"""

    _key = "k.mock"

    def create_key(self) -> str:
        return self._key

    def is_key(self, token: str) -> bool:
        if token.startswith("k."):
            return True
        return False

    def validate(self, token: str) -> Principal:
        if self._key == token:
            return Principal(
                email="tom@myspace.com",
                display_name="tom",
                picture="https://i.insider.com/4efd9b8b69bedd682c000022?width=750&format=jpeg&auto=webp",
            )
        raise Exception("Invalid token")


class HubKeyProvider(KeyProvider, WithDB):
    """AgentSea Hub provider"""

    def __init__(self) -> None:
        self.hub_url = os.environ.get("AGENTSEA_HUB_URL")
        if not self.hub_url:
            raise ValueError(
                "$AGENTSEA_HUB_URL must be set to user the Hub key provider"
            )

    def create_key(self) -> str:
        raise NotImplemented()

    def is_key(self, token: str) -> bool:
        if token.startswith("k."):
            return True
        return False

    def validate(self, token: str) -> Principal:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(f"{self.hub_url}/v1/users/me", headers=headers)
            response.raise_for_status()  # Raise an HTTPError if one occurred.

            user_data = response.json()
            # print("key response user data: ", user_data)
            prof = V1Principal(**user_data)
            # print("returning profile: ", prof)
            out = Principal.from_v1_schema(prof)
            if not out:
                raise ValueError("Could not parse user from schema")
            print("returning user: ", out)
            return out

        except RequestException as e:
            raise ValueError(f"Failed to validate token. Error: {e}")


def get_key() -> Optional[str]:
    return os.environ.get("AGENTSEA_KEY")


def ensure_key() -> str:
    key = get_key()
    if not key:
        raise ValueError("$AGENTSEA_KEY must be provided to use hub components")
    return key


def default_key_provider() -> KeyProvider:
    return HubKeyProvider()
