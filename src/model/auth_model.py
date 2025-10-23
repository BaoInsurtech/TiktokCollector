from pydantic import BaseModel

class AuthTokenResponse(BaseModel):
    access_token: str
    access_token_expire_in: int
    refresh_token: str
    refresh_token_expire_in: int

class ShopDataResponse(BaseModel):
    shop_id: int
    shop_name: str
    shop_code: str
    shop_cipher: str