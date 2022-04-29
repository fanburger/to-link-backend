from sqlmodel import Session, select

from app.sql.models import UserInDB, OpenidSessionkey, AddressInDB


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


def add_new_address(db: Session, new_address: AddressInDB):
    """"
    """

    db.add(new_address)
    db.commit()


def select_address_by_phonenum(db: Session, phone_num: str):
    """通过电话查地址

    :param db:
    :param phone_num:
    :return:
    """
    statement = select(AddressInDB).where(AddressInDB.phone_number == phone_num)
    address = db.exec(statement).first()
    return address


def delete_address_by_id_phonenum(db: Session, aid: int, phone_num: str):
    """考虑到一对多的情况，同时使用id和手机号码来进行删除

    :param db:
    :param aid:
    :param phone_num:
    :return:
    """
    statement = select(AddressInDB).where(AddressInDB.phone_number == phone_num).where(AddressInDB.id == aid)
    results = db.exec(statement)
    abandoned_address = results.one()
    db.delete(abandoned_address)
    db.commit()
    print('删除成功')


def update_address_by_id_phonenum(db: Session, aid: int, phone_num: str, new_address: str):
    """
    
    :param db: 
    :param aid: 
    :param phone_num: 
    :return: 
    """
    statement = select(AddressInDB).where(AddressInDB.phone_number == phone_num).where(AddressInDB.id == aid)
    results = db.exec(statement)
    update_instances = results.one()
    update_instances.user_address = new_address
    db.add(update_instances)
    db.commit()
    db.refresh(update_instances)
    print("修改成功！")
