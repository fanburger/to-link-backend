from sqlmodel import SQLModel


class Code2SessionReq(SQLModel):
    appid: str
    secret: str
    js_code: str
    grant_type: str = 'authorization_code'


class Code2SessionRsp(SQLModel):
    openid: str | None
    session_key: str | None
    unionid: str | None
    errcode: int | None
    errmsg: str | None
