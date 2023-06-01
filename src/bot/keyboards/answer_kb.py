from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.callback_factories import QuestionCallbackFactory
from src.bot.lexicon import render_template


async def send_question(test, message=None, callback=None):
    test_example = list(test.test.items())[test.question]

    answers = [InlineKeyboardButton(
        text=i + 1,
        callback_data=QuestionCallbackFactory(test_id=test.test_id, action='next', value=v).pack()) for i, v in
        enumerate(list(test_example[1].values()))
    ]

    cancel: InlineKeyboardButton = InlineKeyboardButton(
        text='❌ Отменить тест',
        callback_data='stop')

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[answers, [cancel]])

    text = render_template("test.html",
                           question=test.question,
                           score=test.score,
                           question_text=test_example[0],
                           number_of_questions=test.number_of_questions,
                           answers=[i[0]
                                    for i in list(test_example[1].items())],
                           )

    if callback:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    elif message:
        await message.answer(text=text, reply_markup=keyboard)
