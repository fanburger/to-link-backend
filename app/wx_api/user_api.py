from fastapi import status
from httpx import AsyncClient, Response

from app.wx_api.api_models import Code2SessionReq, Code2SessionRsp
from app.config import MINIPROGRAM_APPID, MINIPROGRAM_SECRET, CODE2SESSION_URL


async def code2session(code: str) -> Code2SessionRsp:
    """用小程序生成的 code 换取 openid 和 session_key

    详见: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html

    :param code: 登录时获取的 code
    :return: app.wx_api.api_models.Code2SessionRsp
    """
    c2sreq = Code2SessionReq(appid=MINIPROGRAM_APPID, secret=MINIPROGRAM_SECRET, js_code=code)
    async with AsyncClient() as client:
        rsp: Response = await client.get(url=CODE2SESSION_URL, params=c2sreq.dict())
        if rsp.status_code == status.HTTP_200_OK:
            return Code2SessionRsp(**rsp.json())
