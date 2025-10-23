from pydantic import BaseModel

class APIResponse(BaseModel):
    code: int
    message: str
    data: dict | list | None = None