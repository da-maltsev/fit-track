from typing import Literal

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"  # noqa: S105


class TokenData(BaseModel):
    user_id: str | None = None
