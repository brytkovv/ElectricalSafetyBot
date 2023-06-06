""" This file represents a stop logic """

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.filters import Text
from aiogram.types import CallbackQuery

from src.bot.callback_factories.question import QuestionCallbackFactory

stop_router = Router(name="stop")


@stop_router.message(Command(commands="stop"))
async def stop(message: types.Message, db):
    """stop command handler"""
    test = await db.test.get(message.from_user.id)
    
    if not test.status:
        return await message.answer("⁉️ Нет активных тестов")

    await db.attempt.new(attempt_id=test.test_id, user_id=message.from_user.id, result=0.0)
    await db.test.update(
        user_id=message.from_user.id,
        status=False,
        question=0,
        score=0
    )
    await db.session.commit()

    return await message.answer("❌ Тест успешно отменен")


@stop_router.callback_query(QuestionCallbackFactory.filter(F.action == "stop") or Text(text='stop'))
async def cancel_the_test(
        callback: CallbackQuery,
        callback_data: QuestionCallbackFactory,
        db  
):
    test = await db.test.get(callback.message.chat.id)
    
    if not test or test.test_id != callback_data.test_id:
        await callback.message.edit_text(
            text='⁉️ Теста не существует'
        )
    else:
        await db.attempt.new(attempt_id=test.test_id, user_id=callback.message.chat.id, result=0.0)
        await db.test.update(
            user_id=callback.message.chat.id,
            status=False,
            question=0,
            score=0
        )

        await db.session.commit()
        await callback.message.edit_text(
            text='❌ Тест отменен'
        )
