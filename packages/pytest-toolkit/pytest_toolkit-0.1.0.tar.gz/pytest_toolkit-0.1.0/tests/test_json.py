from pytest_toolkit import get_diff


def test_correct_comparasion():
    """
    Название файла есть, поэтому ищем файл по названию. Такой файл один.
    """
    assert (
        get_diff(
            result_dict={"example1": "example1"}, filename="correct_comparasion.json"
        )
        == {}
    )


def test_filename_search():
    """
    Названия файла нет, поэтому ищем файл по названию функции.
    Таких файлов несколько, поэтому выбираем тот, который лежит
    в директории json
    """
    assert get_diff(result_dict={"example2": "example2"}) == {}
