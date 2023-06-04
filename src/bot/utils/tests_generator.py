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
    file = Path(*file.split('/'))

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
