from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.enum_base.enums import UserPurview
from app.public_models import Token
from app.routers.user_model import UserSignUpReq
from app.sql.crud import is_existed_phone, add_user, add_openid_session, get_user_by_phone_number
from app.sql.database import gen_session
from app.sql.models import UserInDB, OpenidSessionkey
from app.wx_api.user_api import code2session
from app.dependencies import hash_password, create_access_token, verify_password

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/signup', response_model=Token, summary='注册')
async def create_user(info: UserSignUpReq, db: Session = Depends(gen_session)):
    """用户注册 , 新建用户

    支持用户通过手机号和密码的方式注册
    """
    if is_existed_phone(db, info.phone_number):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='用户已存在')

    auth_response = await code2session(info.code)
    if not all([auth_response.openid, auth_response.session_key]):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='code 错误')

    hashed_password = hash_password(info.password)
    user = UserInDB(**info.dict(), openid=auth_response.openid, hashed_password=hashed_password)
    token_payload = dict(**auth_response.dict(), **info.dict(), purview=UserPurview.publish.value)
    token = create_access_token(token_payload)

    try:
        add_openid_session(db, OpenidSessionkey(**auth_response.dict()))
        add_user(db, user)
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.commit()

    return token


@router.post('/phone_login', response_model=Token, summary='手机号登录')
async def login_by_phone(db: Session = Depends(gen_session), form_data: OAuth2PasswordRequestForm = Depends()):
    """用户账号密码登录接口

    该接口仅供账号密码登录调用 , 请求头中`Content-Type`请使用`application/x-www-form-urlencoded`
    """
    if not (user := get_user_by_phone_number(db, form_data.username)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='密码错误')

    token = create_access_token(user.dict())

    return token
