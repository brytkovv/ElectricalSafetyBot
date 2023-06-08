from sqlalchemy import MetaData

from src.db import Database
from src.db.models.base import Base


class MockedDatabase(Database):  # TODO: зачем нам тирдаун???? если мы не делаем коммит данные не меняются, другой вопрос, что мы тестируем на рабочей дб
    async def teardown(self):    # он удаляет все после тестов, даже не до
        """Clear all data in the database"""
        metadata: MetaData = Base.metadata
        for table in metadata.tables.values():
            await self.session.execute(table.delete())
        await self.session.commit()
