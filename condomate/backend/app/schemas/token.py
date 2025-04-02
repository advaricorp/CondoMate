from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    username: str | None = None

class TokenPayload(BaseModel):
    sub: str
    email: str
    tenant_id: str
    type: str | None = None  # "refresh" for refresh tokens, None for access tokens 