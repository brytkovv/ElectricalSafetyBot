""" Chat model file """

import uuid

from sqlalchemy import Column, Integer, ForeignKey, BigInteger, String, Boolean, UUID
from sqlalchemy import JSON

from src.db.models import Base


class TestStatus(Base):
    __tablename__ = 'TestStatus'

    user_id = Column(BigInteger, ForeignKey('User.user_id'), primary_key=True)
    test_id = Column(UUID, default=uuid.uuid4())
    status = Column(Boolean, default=False)
    theme = Column(String, default='src/bot/utils/data_4.json')
    number_of_questions = Column(Integer, default=10)
    show_correct_anwser_alert = Column(Boolean, default=True)
    test = Column(JSON, default={})
    question = Column(Integer, default=0)
    score = Column(Integer, default=0)

    def __repr__(self):
        return self.status
