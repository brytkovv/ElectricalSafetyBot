import uuid

from aiogram.filters.callback_data import CallbackData

# TODO: скоро не будет использоваться в аиограме
class QuestionCallbackFactory(CallbackData, prefix='quest'):
    test_id: uuid.UUID
    action: str
    value: int
