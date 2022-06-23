from enum import Enum


class Errors(Enum):
    ERROR_INCORRECT_MARQUE_AUTO = -1  # Неверная марка автомобиля (данной марки нет)
    ERROR_INCORRECT_MODEL_AUTO = -2  # Неверная модель авто
    ERROR_INCORRECT_CITY = -3   # Неверный город
    ERROR_MODEL_WITHOUT_MARQUE = -4  # Задана модель без марки

