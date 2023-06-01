import json
from operator import sub
from pathlib import Path
from random import sample


def round_and_checking(lst, n):
    """
    Подбираем целое число вопросов для каждой темы
    используется рекурсивная функция
    :param lst:
    :param n:
    :return:
    """
    # округляем доли тем
    upd_lst = [round(i) for i in lst]
    # разница между долей и ее округленным значением
    lst_diff = [abs(sub(*i)) for i in zip(lst, upd_lst)]

    if sum(upd_lst) == n:
        return upd_lst

    elif sum(upd_lst) > n:
        lst[lst_diff.index(max(lst_diff))] = round(
            lst[lst_diff.index(max(lst_diff))]) - 1
        return round_and_checking(lst, n)

    elif sum(upd_lst) < n:
        lst[lst_diff.index(max(lst_diff))] = round(
            lst[lst_diff.index(max(lst_diff))]) + 1
        return round_and_checking(lst, n)


def generate_the_test(file, n):
    """
    Для конкретного файла
    выбираем количество вопросов каждой темы
    и выводим списком

    :param file: str название файла
    :param n: int колиество вопросов
    :return: list список кварг с вопросами и ответами, n- количество вопросов
    """
    file = Path(*file.split('/'))  # TODO: в тестах не работает этот относительный адрес

    with open(file, encoding='utf8') as file:
        data = json.load(file)

    # Суммарная количество вопросов
    summary_lenght = sum([len(i.items()) for i in data])

    if n > summary_lenght:
        n = summary_lenght

    # Количество вопросов в каждой теме
    element_lenght = [(len(i.items()) / summary_lenght) * n for i in data]
    # Доля каждой темы
    adjust_proportion = [1 if i <= 1 else i for i in element_lenght]

    tasks_amount = round_and_checking(adjust_proportion, n)

    out = [sample(list(el.items()), k=tasks_amount[i])
           for i, el in enumerate(data)]
    return {j[0]: j[1] for i in out for j in i}, n


# TODO оформить как тест, добавить проверки
def test_len_of_the_list(min, max, file):
    for i in range(min, max):  # 0,1,2,3 - не подходит
        output = generate_the_test(file, i)
        try:
            assert len(output) == i, f'Длина не соответствует в строке {i}'
            assert type(output) == dict, f'Ответы не в виде словаря{i}'
        except AssertionError as e:
            print(e, type(e), sep='\n')


# проверяем что билеты не совпадают
def test_lists_not_equals(file, n):
    one = generate_the_test(file, n)
    two = generate_the_test(file, n)
    try:
        assert one != two, 'Генерируются одинаковые тесты'
    except AssertionError as e:
        print(e, type(e))

# test_len_of_the_list(4, 100, 'data_3.json')
# test_lists_not_equals('data_3.json', 10)

# out = generate_the_test()
