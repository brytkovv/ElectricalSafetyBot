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


class Database:
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
