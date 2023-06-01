""" Attempts repository file """
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Attempt, User
from src.db.repositories import Repository


class AttemptRepo(Repository[Attempt]):
    """
    Attempts repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize attempt repository

        """
        super().__init__(type_model=Attempt, session=session)

    async def new(
            self,
            attempt_id: str,
            user_id: int,
            result: float,
            test_name: str = ''
    ):
        """
        Insert a new user into the database
        """
        new_att = await self.session.merge(
            Attempt(
                attempt_id=attempt_id,
                user_id=user_id,
                test_name=test_name if test_name else '',
                result=result
            )
        )
        return new_att

    async def get_stat(self, user_id: int):
        """
        All attempts of the user
        :param user_id:
        :return:
        """
        statement = select(self.type_model).where(self.type_model.user_id == user_id)
        await self.session.execute(statement)
        return (await self.session.scalars(statement)).all()

    async def get_top(self):
        """
        Take list of the top-5 users
        :return:
        """
        statement = select(User.user_name, func.count(self.type_model.attempt_id)).join_from(self.type_model,
                                                                                             User).group_by(
            User.user_name).order_by(func.count(self.type_model.attempt_id).desc()).limit(5)
        res = await self.session.execute(statement)

        return res.all()
