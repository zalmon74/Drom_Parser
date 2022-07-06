from enum import Enum


class Errors(Enum):
    ERROR_INCORRECT_MARQUE_AUTO = -1  # Неверная марка автомобиля (данной марки нет)
    ERROR_INCORRECT_MODEL_AUTO = -2  # Неверная модель авто
    ERROR_INCORRECT_CITY = -3   # Неверный город
    ERROR_MODEL_WITHOUT_MARQUE = -4  # Задана модель без марки
    ERROR_INCORRECT_GET_PARAMETER = -5  # Заданный параметр отсутствует или недоступен
    ERROR_INCORRECT_COUNT_ARG_FOR_GET_PARAMETER = -6  # Данный параметр может иметь только один аргумент
    ERROR_INCORRECT_ARGUMENT_FOR_GET_PARAMETER = -7  # Данный параметр не может иметь такой аргумент
