from sqlmodel import Session, select

from app.sql.models import UserInDB, OpenidSessionkey


def is_existed_phone(db: Session, phone_number: str) -> bool:
    """检查数据库中是否存在指定的手机号

    :param db: sqlmodel.Session
    :param phone_number: eg:18888888888
    :return: True or False
    """
    statement = select(UserInDB.phone_number).where(UserInDB.phone_number == phone_number)
    phone = db.exec(statement).first()
    return True if phone else False


def add_user(db: Session, new_user: UserInDB) -> None:
    """添加一个新用户

    注: 出于注册流程原子化问题 , 此处不能 commit

    :param db: sqlmodel.Session
    :param new_user: app.sql.models.UserInDB()
    :return: None
    """
    db.add(new_user)


def add_openid_session(db: Session, info: OpenidSessionkey) -> None:
    """写入 openid 对应的 session_key

    注: 出于注册流程原子化问题 , 此处不能 commit

    :param db: sqlmodel.Session
    :param info: app.sql.models.OpenidSessionkey()
    :return: None
    """
    db.add(info)


def get_user_by_phone_number(db: Session, phone: str) -> UserInDB:
    """通过手机号查询用户信息

    :param db: sqlmodel.Session
    :param phone: 用户手机号
    :return: app.sql.models.UserInDB()
    """
    statement = select(UserInDB).where(UserInDB.phone_number == phone)
    user = db.exec(statement).first()
    return user


def get_user_by_openid(db: Session, openid: str) -> UserInDB:
    """通过 openid 查询用户

    :param db: sqlmodel.Session
    :param openid: 用户 openid
    :return: app.sql.models.UserInDB()
    """
    statement = select(UserInDB).where(UserInDB.openid == openid)
    user = db.exec(statement).first()
    return user


def update_session_key(db: Session, info: OpenidSessionkey) -> None:
    """更新 session_key

    :param db: sqlmodel.Session
    :param info: app.sql.models.OpenidSessionkey()
    :return: None
    """
    statement = select(OpenidSessionkey).where(OpenidSessionkey.openid == info.openid)
    openid_sessionkey = db.exec(statement).first()

    openid_sessionkey.session_key = info.session_key
    db.add(openid_sessionkey)
