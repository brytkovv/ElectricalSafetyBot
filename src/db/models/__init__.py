"""
    Init file for models namespace
"""
from src.db.models.attempts import Attempt
from src.db.models.base import Base
from src.db.models.status_of_the_test import TestStatus
from src.db.models.user import User

__all__ = [Base, TestStatus, User, Attempt]
