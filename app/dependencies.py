from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import jwt

from app.public_models import TokenPayload, Token
from app.config import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_DAYS, ALGORITHM

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password: str) -> str:
    """
    返回字符串 hash 值
    :param password: 明文密码
    :return: hashed_str
    """
    return pwd_context.hash(password)


def create_access_token(payload: dict, expire_delta: timedelta | None = None) -> Token:
    """
    创建 token
    :param payload: token 承载的内容 (必须包含:app.public_models.TokenPayload 所需的字段)
    :param expire_delta: token 有效期
    :return: app.public_models.Token()
    """
    to_encode = payload.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.setdefault('exp', expire)
    to_encode = TokenPayload(**to_encode).dict()  # 校验和过滤相关值
    jwt_encode = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=jwt_encode)
