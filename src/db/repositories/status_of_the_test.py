""" Test repository file """
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.utils import generate_the_test
from src.db.models import TestStatus
from src.db.repositories import Repository


class RepoTest(Repository[TestStatus]):
    """
    Chat repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize test repository
        """
        super().__init__(type_model=TestStatus, session=session)

    async def new(
            self,
            user_id: int,
            theme: str = 'src/bot/utils/data_4.json',
            questions: int = 10
    ):
        """
        Insert a new test into the database
        :param user_id: Telegram user id
        :param theme: theme of the test
        :param test: as
        """
        new_test = await self.session.merge(
            TestStatus(
                user_id=user_id,
                test=generate_the_test(file=theme, n=questions),
                number_of_questions=questions
            )
        )
        return new_test
