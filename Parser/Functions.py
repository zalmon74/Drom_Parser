from requests import get, Response


def get_request(url: str, headers: dict, parameters: dict = None) -> Response:
    """
    Функция делает GET запрос на указанный URL с указанными загаловками и параметрами
    :param url: URL-адрес
    :param headers: словарь с заголовками
    :param parameters: словарь с параметрами
    :return:
    """
    response = get(url, headers=headers, params=parameters)
    return response


def print_sorted_dict_with_separator(d_print: dict, separator: str = '|'):
    """
    Метод печати словаря вида: key 'separator' data
    :param d_print: Словарь, который необходимо напечатать
    :param separator: Разделитеть при печати между key и data
    """
    for key, data in sorted(d_print.items()):
        print(f'{key} {separator} {data}')
