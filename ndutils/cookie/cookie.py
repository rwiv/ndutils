from pydantic import BaseModel, Field
from nodriver.cdp.network import CookieParam


class Cookie(BaseModel):
    name: str
    value: str
    url: str | None = None
    domain: str | None = None
    path: str | None = None
    size: int | None = None
    http_only: bool | None = Field(alias="httpOnly", default=None)
    secure: bool | None = None
    session: bool | None = None
    priority: str | None = None
    same_party: bool | None = Field(alias="sameParty", default=None)
    source_scheme: str | None = Field(alias="sourceScheme", default=None)
    source_port: int | None = Field(alias="sourcePort", default=None)
    expires: float | None = None
    same_site: str | None = Field(alias="sameSite", default=None)

    def to_cookie_param(self) -> CookieParam:
        return CookieParam.from_json(self.model_dump(mode="json"))
