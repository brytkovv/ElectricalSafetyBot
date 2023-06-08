""" Database class with all-in-one features """
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

from src.configuration import conf
from src.db.models import Base
from src.db.repositories import UserRepo, RepoTest, AttemptRepo


async def create_async_engine(url: URL | str) -> AsyncEngine:
    """
    :param url:
    :return:
    """
    engine = _create_async_engine(
        url=url, echo=conf.debug, pool_pre_ping=True
    )

    # TODO: сделать алембик и убрать это
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine


async def create_session_maker(engine: AsyncEngine = None) -> sessionmaker:
    """
    :param engine:
    :return:
    """
    return sessionmaker(
        engine or await create_async_engine(conf.db.build_connection_str()),
        class_=AsyncSession,
        expire_on_commit=False,
    )


class Singleton(type): # TODO: проверить, работает или нет (для тестов)
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Database(metaclass=Singleton):
    """
    Database class is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions
    """

    user: UserRepo
    """ User repository """
    test: RepoTest
    """ Test repository """
    attempt: AttemptRepo
    """ Attempt repository """

    session: AsyncSession

    def __init__(
            self, session: AsyncSession, user: UserRepo = None, test: RepoTest = None, attempt: AttemptRepo = None
    ):
        self.session = session
        self.user = user or UserRepo(session=session)
        self.test = test or RepoTest(session=session)
        self.attempt = attempt or AttemptRepo(session=session)
