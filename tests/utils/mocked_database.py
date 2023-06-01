from sqlalchemy import MetaData

from src.db import Database
from src.db.models.base import Base


class MockedDatabase(Database):
    async def teardown(self):
        """Clear all data in the database"""
        metadata: MetaData = Base.metadata
        for table in metadata.tables.values():
            await self.session.execute(table.delete())
        await self.session.commit()
