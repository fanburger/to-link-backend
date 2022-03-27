from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session

from app.enum_base.enums import UserPurview
from app.public_models import Token
from app.routers.user_model import UserSignUpReq
from app.sql.crud import is_existed_phone, add_user, add_openid_session
from app.sql.database import gen_session
from app.sql.models import UserInDB, OpenidSessionkey
from app.wx_api.user_api import dev_code2session
from app.dependencies import hash_password, create_access_token

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/signup', response_model=Token, description='用户注册(账号,密码)')
async def create_user(info: UserSignUpReq, db: Session = Depends(gen_session)):
    if is_existed_phone(db, info.phone_number):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='用户已存在')

    auth_response = await dev_code2session(info.code)
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
