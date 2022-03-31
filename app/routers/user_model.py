from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    nickname: str
    avatar_url: str


class UserSignUpReq(UserBase):
    phone_number: str = Field(max_length=11, description='仅支持中国大陆地区手机号')
    password: str = Field(min_length=8, max_length=30)
    code: str = Field(description='wx.login 接口返回的code')


class LoginByOpenidReq(SQLModel):
    code: str


class PhoneNumberLogin(SQLModel):
    phone_number: str = Field(max_length=11, description='仅支持中国大陆地区手机号')
    password: str = Field(min_length=8, max_length=30)
