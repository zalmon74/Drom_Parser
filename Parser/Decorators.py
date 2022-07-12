"""
Данный файл содержит различные декораторы для парсера
"""


def print_symbol(f_print: bool, symbol: str):
    """
    Декоратор, который печатает определенный символ перед вызовом функций
    :param f_print: Флаг печати, True = символ выводится на экран, False = нет
    :param symbol: Символ, который необходимо вывести на экран
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if f_print:
                print(symbol, end='')
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
