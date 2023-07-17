""" Attempts repository file """
from collections import namedtuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Attempt, User
from src.db.repositories import Repository

UserRank = namedtuple('UserRank', ['rank', 'name', 'record', 'id'], defaults=(None,))


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

    async def get_record(self, user_id: int):
        """
        All attempts of the user
        :param user_id:
        :return:
        """
        statement = select(self.type_model).where(self.type_model.user_id == user_id)
        await self.session.execute(statement)
        res = (await self.session.scalars(statement)).all()

        return len(res), sum([0 if i.result < 0.8 else 1 for i in res])

    async def get_top(self, user_id: int):
        """
        Take list of the top-5 users
        :return:
        """
        statement = select(
            User.user_name, func.count(self.type_model.attempt_id), self.type_model.user_id) \
            .join_from(self.type_model, User) \
            .group_by(User.user_name, self.type_model.user_id) \
            .order_by(func.count(self.type_model.attempt_id).desc()
                      )
        res = await self.session.execute(statement)
        result = [UserRank(i[0], *i[1]) for i in list(enumerate(res.all(), 1))]

        if user_id not in [user.id for user in result[:5]]:
            user_rank = [user for user in result if user_id == user.id]
            return result[:5] + user_rank
        else:
            return result[:5]

    async def get_num_of_attempts(self):
        statement = select(func.count(self.type_model.attempt_id))
        res = await self.session.execute(statement)

        return res.one_or_none()
