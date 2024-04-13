"""Schema for neosctl."""

import configparser
import dataclasses
from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator


class Auth(BaseModel):
    access_token: str = ""
    expires_in: Optional[int] = None
    refresh_token: str = ""
    refresh_expires_in: Optional[int] = None


class OptionalProfile(BaseModel):
    gateway_api_url: str = ""
    registry_api_url: str = ""
    iam_api_url: str = ""
    hub_api_url: str = ""
    storage_api_url: str = ""
    user: str = ""
    access_token: str = ""
    refresh_token: str = ""
    ignore_tls: bool = False
    account: str = ""


class Profile(OptionalProfile):
    gateway_api_url: str
    registry_api_url: str = ""
    iam_api_url: str = ""
    hub_api_url: str = ""
    storage_api_url: str
    user: str
    access_token: str
    refresh_token: str
    ignore_tls: bool
    account: str = "root"  # backwards compat default


class Core(BaseModel):
    name: str
    host: str
    account: Optional[str] = None
    active: bool = False

    @field_validator("account", mode="before")
    @classmethod
    def convert_null_account(cls: "type[Core]", v: str) -> Optional[str]:
        """Toml treats None as "null", convert back to None."""
        if v == "null":
            return None
        return v


class Env(BaseModel):
    name: str
    hub_api_url: str
    user: str
    access_token: str
    refresh_token: str
    ignore_tls: bool
    active: bool
    account: str = "root"
    cores: dict[str, Core] = Field(default_factory=dict)


class Credential(BaseModel):
    access_key_id: str
    secret_access_key: str


@dataclasses.dataclass
class Common:
    gateway_api_url: str
    hub_api_url: str
    storage_api_url: str
    profile_name: str
    config: configparser.ConfigParser
    env: configparser.ConfigParser
    credential: configparser.ConfigParser
    active_env: Optional[Env] = None
    active_core: Optional[Core] = None
    profile: Optional[Union[Profile, OptionalProfile]] = None

    def get_account(self) -> str:
        """Return system account."""
        if self.active_env:
            return self.active_env.account

        if self.profile:
            return self.profile.account

        return "root"

    def get_gateway_api_url(self) -> str:
        """Return gateway api url.

        If a user profile is provided and defines a gateway url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.active_core:
            return self.active_core.host

        if self.profile and self.profile.gateway_api_url:
            return self.profile.gateway_api_url
        return self.gateway_api_url

    def get_storage_api_url(self) -> str:
        """Return storage api url.

        If a user profile is provided and defines a storage url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.active_core:
            return self.active_core.host.replace("://", "://saas.").replace("/api/gateway", "")

        if self.profile and self.profile.storage_api_url:
            return self.profile.storage_api_url
        return self.storage_api_url

    def get_hub_api_url(self) -> str:
        """Return hub api url.

        If a user profile is provided and defines a hub url, return that,
        otherwise fall back to cli defined default.
        """
        if self.active_env:
            return self.active_env.hub_api_url

        if self.profile and self.profile.hub_api_url:
            return self.profile.hub_api_url

        if self.profile and self.profile.iam_api_url:
            url = self.profile.iam_api_url
            url = url.replace("/api/iam", "/api/hub")
            return url.replace("/api/hub/iam", "/api/hub")

        return self.hub_api_url
