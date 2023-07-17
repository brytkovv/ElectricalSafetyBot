""" User repository file """
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.repositories import Repository


class UserRepo(Repository[User]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize user repository as for all users or only for one user
        """
        super().__init__(type_model=User, session=session)

    async def new(
            self,
            user_id: int,
            user_name: str,
    ):
        """
        Insert a new user into the database
        :param user_id: Telegram user id
        :param user_name: Telegram username
        :param first_join_date:
        :param last_visit_date:
        """
        new_user = await self.session.merge(
            User(
                user_id=user_id,
                user_name=user_name,
                first_join_date=datetime.now(),
                last_visit_date=datetime.now()
            )
        )
        return new_user

    async def get_num_of_users(self):
        statement = select(func.count(self.type_model.user_id))
        res = await self.session.execute(statement)

        return res.one_or_none()
