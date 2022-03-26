from datetime import datetime

from sqlmodel import SQLModel


class Token(SQLModel):
    token_type: str = 'bearer'
    access_token: str


class TokenPayload(SQLModel):
    openid: str
    phone_number: str
    purview: int
    exp: datetime
