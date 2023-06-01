import uuid

from aiogram.filters.callback_data import CallbackData


class QuestionCallbackFactory(CallbackData, prefix='quest'):
    test_id: uuid.UUID
    action: str
    value: int
