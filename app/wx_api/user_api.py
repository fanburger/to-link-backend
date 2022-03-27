from fastapi import status
from httpx import AsyncClient, Response

from app.wx_api.api_models import Code2SessionReq, Code2SessionRsp
from app.config import MINIPROGRAM_APPID, MINIPROGRAM_SECRET, CODE2SESSION_URL
from app.dependencies import get_base64, hash_password


async def code2session(code: str) -> Code2SessionRsp:
    """
    用小程序生成的 code 换取 openid 和 session_key

    详见: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html

    :param code: 登录时获取的 code
    :return: app.wx_api.api_models.Code2SessionRsp()
    """
    c2sreq = Code2SessionReq(appid=MINIPROGRAM_APPID, secret=MINIPROGRAM_SECRET, js_code=code)
    async with AsyncClient() as client:
        rsp: Response = await client.get(url=CODE2SESSION_URL, params=c2sreq.dict())
        if rsp.status_code == status.HTTP_200_OK:
            print(rsp.json())
            return Code2SessionRsp(**rsp.json())


async def dev_code2session(code: str) -> Code2SessionRsp:
    """
    模拟通过 code 换取 openid 和 session_key

    注意: 该函数只能用于开发测试 , 并且总是返回成功的情况
    openid 值是用 code 进行 hash 后模拟的
    session_key 值是对 code 进行 base64 编码后的结果

    :param code: 登录时获取的 code
    :return: app.wx_api.api_models.Code2SessionRsp()
    """
    openid = hash_password(code)
    session_key = get_base64(code)
    return Code2SessionRsp(openid=openid, session_key=session_key)
