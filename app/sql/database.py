from sqlmodel import SQLModel, Session, create_engine

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    """创建所有数据库表 , 如果表已经存在则不再创建

    :return: None
    """
    SQLModel.metadata.create_all(engine)


def gen_session() -> Session:
    """生成一个会话实例

    注意: 大多数情况不应该在该函数里面处理异常 , 除非你清楚这样做带来的问题
    同时 , 你能解决这些问题.

    :return: sqlmodel.Session(engine)
    """
    with Session(engine) as session:
        yield session
