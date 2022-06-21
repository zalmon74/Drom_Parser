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
