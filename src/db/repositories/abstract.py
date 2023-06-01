""" Repository file """
import abc
from typing import Generic, List, Type, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Base

AbstractModel = TypeVar("AbstractModel")


class Repository(Generic[AbstractModel]):
    """Repository abstract class"""

    type_model: Type[Base]
    session: AsyncSession

    def __init__(self, type_model: Type[Base], session: AsyncSession):
        """
        Initialize abstract repository class
        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work
        """
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel:
        """
        Get an ONE model from the database with PK
        :param ident: Key which need to find entry in database
        :return:
        """
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, whereclause) -> AbstractModel | None:
        """
        Get an ONE model from the database with whereclause
        :param whereclause: Clause by which entry will be found
        :return: Model if only one model was found, else None
        """
        statement = select(self.type_model).where(whereclause)
        return (await self.session.execute(statement)).one_or_none()

    async def get_many(
            self, whereclause, limit: int = 100, order_by=None
    ) -> List[AbstractModel]:
        """
        Get many models from the database with whereclause
        :param whereclause: Where clause for finding models
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause

        Example:
        >> Repository.get_many(Model.id == 1, limit=10, order_by=Model.id)

        :return: List of founded models
        """
        statement = select(self.type_model).where(whereclause).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()  # noqa

    async def delete(self, user_id) -> None:
        """
        Delete model from the database

        :param user_id: (Optional) Which statement
        :return: Nothing
        """
        statement = delete(self.type_model).where(self.type_model.user_id == user_id)  # noqa
        await self.session.execute(statement)

    async def update(self, user_id: int, **kwargs):
        upd = await self.session.get(entity=self.type_model, ident=user_id)
        statement = update(self.type_model).where(self.type_model.user_id == user_id).values(**kwargs)
        await self.session.execute(statement)
        return upd

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        """
        This method is need to be implemented in child classes,
        it is responsible for adding a new model to the database
        :return: Nothing
        """
        ...
