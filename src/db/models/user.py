""" User model file """
from datetime import datetime

from sqlalchemy import Column, String, DateTime, BigInteger
from sqlalchemy.orm import relationship

from src.db.models import Base


class User(Base):
    __tablename__ = 'User'
    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    user_name = Column(String, nullable=False)
    first_join_date = Column(DateTime, default=datetime.now, nullable=False)
    last_visit_date = Column(DateTime, default=datetime.now, nullable=False)

    record = relationship('Attempt', backref='owner',
                          lazy=True, cascade='all, delete-orphan')

    status = relationship('TestStatus', backref='owner_id',
                          lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.user_id
