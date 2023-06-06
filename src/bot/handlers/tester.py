""" This file represents a tester logic """
import uuid
from datetime import datetime

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from src.bot.callback_factories import QuestionCallbackFactory
from src.bot.keyboards import send_question
from src.bot.utils import generate_the_test
from src.db.models import TestStatus

tester_router = Router(name="test")


@tester_router.callback_query(QuestionCallbackFactory.filter(F.action == "next"))
async def next_quest(
        callback: CallbackQuery,
        callback_data: QuestionCallbackFactory,
        db
):
    async def send_correct_answer():
        text = [k for k, v in list(
            list(test.test.items())[test.question][1].items()) if v == 1][0]
        await callback.answer(
            text=f"❌ Ошибка. Верный ответ: {text if len(text) < 185 else text[:172] + '...'}",
            show_alert=True)
        
    async def correct_answer_alert():
        await callback.answer(
            text=f"✔️ Правильный ответ!", # TODO: вынести текст в шаблоны
            show_alert=True)

    test: TestStatus = await db.test.get(callback.message.chat.id)

    if not test.status or test.test_id != callback_data.test_id:
        return await callback.message.edit_text(
            text='Теста не существует'
        )

    elif test.question + 1 == test.number_of_questions:
        if callback_data.value == 0:
            await send_correct_answer()
        else:
            if test.show_correct_anwser_alert:
                await correct_answer_alert()
            test.score += 1
        result = f'👏 Тест окончен.\nПравильных ответов {test.score} из {test.number_of_questions}'

        await db.attempt.new(attempt_id=test.test_id, user_id=callback.message.chat.id,
                             test_name=test.theme,
                             result=test.score / test.number_of_questions)

        # TODO "Ваши ошибки:" "Ответить повторно на ошибки"

        await callback.message.edit_text(
            text=result
        )

        await db.test.update(
            user_id=callback.message.chat.id,
            status=False,
            question=0,
            score=0
        )
        await db.session.commit()

    else:
        if callback_data.value == 0:
            await send_correct_answer()
            await db.test.update(user_id=callback.message.chat.id, question=test.question + 1, score=test.score)
        else:
            if test.show_correct_anwser_alert:
                await correct_answer_alert()
            await db.test.update(user_id=callback.message.chat.id, question=test.question + 1, score=test.score + 1)
        await db.session.commit()

        await send_question(test=test, callback=callback)


@tester_router.message(Command(commands="test"))
async def process_test_command(message: types.Message, db):
    """test command handler"""
    test: TestStatus = await db.test.get(message.from_user.id)

    test_content, number_of_questions = generate_the_test(file=test.theme, n=test.number_of_questions)

    if not test.status:
        test = await db.test.update(
            user_id=message.from_user.id,
            test_id=uuid.uuid4(),
            status=True,
            number_of_questions=number_of_questions,
            test=test_content
        )

        await db.user.update(user_id=message.from_user.id, last_visit_date=datetime.now())

        await db.session.commit()

        await send_question(test=test, message=message)

    else:
        await message.answer(
            text='Вы уже проходите тест.'
                 'Для отмены теста напишите /stop'
        )
