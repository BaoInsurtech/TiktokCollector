from pydantic import BaseModel

from .auth_model import APIResponse

class AuthTokenResponse(BaseModel):
    access_token: str
    access_token_expire_in: int
    refresh_token: str
    refresh_token_expire_in: int