alreary_testing = 'Вы уже проходите тест.\nДля отмены теста напишите /stop'

correct_answer = f"✔️ Правильный ответ!"

test_not_found = 'Теста не существует'


def the_test_is_over(test):
    return f'👏 Тест окончен.\nПравильных ответов {test.score} из {test.number_of_questions}'


def wrong_answer(text):
    return f"❌ Ошибка. Верный ответ: {text if len(text) < 185 else text[:172] + '...'}"
