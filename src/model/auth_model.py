from pydantic import BaseModel

class AuthTokenResponse(BaseModel):
    access_token: str
    access_token_expire_in: int
    refresh_token: str
    refresh_token_expire_in: int

class ShopDataResponse(BaseModel):
    id: int
    name: str
    region: str
    seller_type: str
    cipher: str
    code: str
