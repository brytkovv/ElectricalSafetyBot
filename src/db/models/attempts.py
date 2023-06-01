""" Attempt model file """
import uuid
from datetime import datetime

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Float, UUID

from src.db.models.base import Base


class Attempt(Base):
    __tablename__ = 'Attempt'

    attempt_id = Column(UUID, default=uuid.uuid4(), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('User.user_id'))
    date = Column(DateTime, default=datetime.now, nullable=False)
    test_name = Column(String, nullable=False, default='bot/utils/data_4.json')
    result = Column(Float, default=0, nullable=False)

    def __repr__(self):  # TODO: не использую
        return str(0 if self.result < 0.8 else 1)
