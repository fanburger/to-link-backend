from sqlmodel import SQLModel, Field

from app.enum_base.enums import UserPurview


class UserInDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nickname: str
    avatar_url: str
    openid: str = Field(index=True)
    phone_number: str = Field(index=True, max_length=11, description='仅支持中国大陆地区手机号')
    hashed_password: str
    purview: int = Field(default=UserPurview.publish.value)
    gender: int | None = Field(default=None)
    sex: int | None = Field(default=None)
    language: str | None = Field(default=None)


class OpenidSessionkey(SQLModel, table=True):
    openid: str = Field(primary_key=True)
    session_key: str


class AddressInDB(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    phone_number: str = Field(max_length=11, description='仅支持中国大陆地区手机号')
    user_address: str = Field(default=None)
