from os import system

from .CLI_Settings.Messages import MESSAGE_INPUT_UNSIGNED_INT_VALUE


def input_unsigned_int(addit_message: str = '', f_clear: bool = True) -> int:
    """
    Метод запроса целого не отрицательного значения от пользователя

    :param addit_message: Дополнительное сообщение при вводе
    :param f_clear: Флаг очистки экрана при запросе значения
    :return: Целое не отрицательное значение, которое ввел пользователь
    """
    result = -1
    while result < 0:
        try:
            if f_clear:
                system('clc||clear||CLS')
            result = input(f'{addit_message}\n\n{MESSAGE_INPUT_UNSIGNED_INT_VALUE}')
            result = int(result)
        except ValueError:
            result = -1
    return result
