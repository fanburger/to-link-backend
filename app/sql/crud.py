from sqlmodel import Session, select

from app.sql.models import UserInDB, OpenidSessionkey


def is_existed_phone(db: Session, phone_number: str) -> bool:
    """
    检查数据库中是否存在指定的手机号
    :param db: sqlmodel.Session
    :param phone_number: eg:18888888888
    :return: True or False
    """
    statement = select(UserInDB.phone_number).where(UserInDB.phone_number == phone_number)
    phone = db.exec(statement).first()
    return True if phone else False


def add_user(db: Session, new_user: UserInDB) -> None:
    """
    添加一个新用户

    注: 出于注册流程原子化问题 , 此处不能 commit
    :param db: sqlmodel.Session
    :param new_user: app.sql.models.UserInDB()
    :return: None
    """
    db.add(new_user)


def add_openid_session(db: Session, info: OpenidSessionkey) -> None:
    """
    写入 openid 对应的 session_key

    注: 出于注册流程原子化问题 , 此处不能 commit
    :param db: sqlmodel.Session
    :param info: app.sql.models.OpenidSessionkey()
    :return: None
    """
    db.add(info)
