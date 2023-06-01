import pytest

from src.bot.utils import generate_the_test


@pytest.mark.parametrize(
    "min,max,file",
    [
        pytest.param(4, 150, 'src/bot/utils/data_3.json'),
        pytest.param(4, 200, 'src/bot/utils/data_4.json'),
        pytest.param(4, 200, 'src/bot/utils/data_5.json')
    ],
)
def test_len_of_the_list(min, max, file):
    for i in range(min, max):  # 0,1,2,3 - не подходит
        data, lenght = generate_the_test(file, i)

        assert lenght == i == len(data), f'Длина не соответствует в строке {i}'
        assert type(data) == dict, f'Ответы не в виде словаря в строке {i}'


@pytest.mark.parametrize(
    "file,n",
    [
        pytest.param('src/bot/utils/data_3.json', 20),
        pytest.param('src/bot/utils/data_4.json', 10),
        pytest.param('src/bot/utils/data_5.json', 100)
    ],
)
def test_lists_not_equals(file, n):
    one_data, _ = generate_the_test(file, n)
    two_data, _ = generate_the_test(file, n)
    assert one_data != two_data, 'Генерируются одинаковые тесты'
