"""
Данный файл содержит возможные дополнительные Get-параметры для запроса
"""

from datetime import datetime


class BaseParameter:
    """
    Базовый класс для параметров
    """

    def get_name_str(self):
        """
        Виртуальный метод, для получения имени параметра для поиска

        :return: строку с именем параметра
        """
        raise NotImplementedError('Чисто виртуальный метод')

    def get_list_parameters(self):
        """
        Виртуальный метод, для получения списка стандартных значений данного параметра

        :return: список стандартных значений
        """
        raise NotImplementedError('Чисто виртуальный метод')

    def get_dict_parameters(self):
        """
        Виртуальный метод, для получения словаря, где key = имя параметры, data = список стандартных параметров

        :return: словарь, где key = имя параметры, data = список стандартных параметров
        """
        raise NotImplementedError('Чисто виртуальный метод')

    def is_more_arg(self):
        """
        Виртуальный метод, для определения возможности параметра иметь несколько значений

        :return: True = параметр может иметь несколько значений, False = параметр не может иметь несколько значений
        """
        raise NotImplementedError('Чисто виртуальный метод')

    def is_arbitrary_arg(self):
        """
        Виртуальный метод, для определения возможности параметра иметь произвольное значение аргумента

        :return: True = параметр может иметь произв. значение, False = параметр не может иметь произв. значение
        """
        raise NotImplementedError('Чисто виртуальный методдд')


class ParameterDistance(BaseParameter):
    """
    Параметр позволяет искать объявления с дополнительным расстоянием поиска от основного города.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольные
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = True
    # Стандартные значения увеличения поиска
    d_100 = 100
    d_200 = 200
    d_500 = 500
    d_1000 = 1000
    # Имя параметра
    name = 'distance'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.d_100, self.d_200, ParameterDistance.d_500, ParameterDistance.d_1000]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMinPrice(BaseParameter):
    """
    Параметр позволяет искать объявления с определенной минимальной стоимостью авто.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольные
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = True
    # Список со стандартными минимальными значениями
    l_min_price = range(50_000, 2_000_001, 50_000)
    # Имя параметра
    name = 'minprice'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [*self.l_min_price]

    def get_dict_parameters(self):
        return {self.name: self.l_min_price}

    def is_more_arg(self):
        return ParameterMinPrice._f_more_arg

    def is_arbitrary_arg(self):
        return ParameterMinPrice._f_arbitrary_arg


class ParameterMaxPrice(BaseParameter):
    """
    Параметр позволяет искать объявления с определенной максимальной стоимостью авто.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольные
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = True
    # Список со стандартными максимальными значениями
    l_max_price = range(50_000, 2_000_001, 50_000)
    # Имя параметра
    name = 'maxprice'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [*self.l_max_price]

    def get_dict_parameters(self):
        return {self.name: self.l_max_price}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMinYear(BaseParameter):
    """
    Параметр позволяет искать объявления от определенного минимального года.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольными
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Список со стандартными минимальными значениями года
    l_min_year = range(1940, datetime.now().year+1, 1)
    # Имя параметра
    name = 'minyear'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [*self.l_min_year]

    def get_dict_parameters(self):
        return {self.name: self.l_min_year}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMaxYear(BaseParameter):
    """
    Параметр позволяет искать объявления от определенного минимального года.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольными
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Список со стандартными минимальными значениями года
    l_max_year = range(1940, datetime.now().year+1, 1)
    # Имя параметра
    name = 'maxyear'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [*self.l_max_year]

    def get_dict_parameters(self):
        return {self.name: self.l_max_year}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterTransmission(BaseParameter):
    """
    Параметр позволяет искать объявления с определенной коробкой передач.
    Может быть выбрано, несколько коробок передач для поиска.

    P.S. На сайте для гибридного авто с АКПП и просто авто АКПП имеются разные параметры
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = True
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    manual = 1  # Механическая КП
    automatic_hybrid = 5  # АКПП для гибридного авто
    automatic = 2  # АКПП
    robotic = 4  # Робот
    vsd = 3  # Вариатор
    # Не указана
    not_specified = -1
    # Имя
    name = 'transmission[]'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.manual, self.automatic_hybrid, self.automatic, self.robotic, self.vsd, self.not_specified]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg

    def get_dict_only_automatic(self):
        """
        Метод возвращает словарь с параметрами для запроса авто с АКПП.

        TODO: Отдельный метод необходимы из-за специфики параметров, которая описана в комментариях к самому параметру

        :return: возвращает словарь, где key = имя параметра, data = список со значениями для запроса
        """
        return {self.name: [self.automatic_hybrid, self.automatic]}

    def get_dict_all_automatic(self):
        """
        Метод возвращает словарь с параметрами для запроса авто со всеми видами КП, кроме механики

        :return: возвращает словарь, где key = имя параметра, data = список со всеми значениями для запроса авто с
                 автоматическими коробками передач (АКПП, робот, вариатор)
        """
        return {self.name: [self.automatic_hybrid, self.automatic, self.robotic, self.vsd]}


class ParameterFuelType(BaseParameter):
    """
    Параметр позволяет искать авто с определенным типом топлива
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    gasoline = 1  # Бензин
    diesel = 2  # Дизель
    electric = 4  # Электро
    hybrid = 5  # Гибридн
    hbo = 6  # ГБО
    # Имя
    name = 'fueltype'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.gasoline, self.diesel, self.electric, self.hybrid, self.hbo]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMinEngineCapacity(BaseParameter):
    """
    Параметр позволяет искать авто с определнным минимальный объемом двигателя
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Список с допустимыми значениями
    min_v = [0.7, 0.8, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.2, 2.3, 2.4, 2.5, 2.7, 2.8,
             3.0, 3.2, 3.3, 3.5, 3.6, 4.0, 4.2, 4.4, 4.5, 4.6, 4.7, 5.0, 5.5, 5.7, 6.0]
    # Имя
    name = 'mv'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return self.min_v

    def get_dict_parameters(self):
        return {self.name: self.min_v}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMaxEngineCapacity(BaseParameter):
    """
    Параметр позволяет искать авто с определнным минимальный объемом двигателя
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Список с допустимыми значениями
    max_v = [0.7, 0.8, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.2, 2.3, 2.4, 2.5, 2.7, 2.8,
             3.0, 3.2, 3.3, 3.5, 3.6, 4.0, 4.2, 4.4, 4.5, 4.6, 4.7, 5.0, 5.5, 5.7, 6.0]
    # Имя
    name = 'xv'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return self.max_v

    def get_dict_parameters(self):
        return {self.name: self.max_v}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterWheelDrive(BaseParameter):
    """
    Параметр позволяет искать авто с определенным типо привода автомобиля
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    front_wheel = 1  # Передний привод
    back_wheel = 2  # Задний привод
    wd_4 = 3  # 4WD
    # Имя
    name = 'privod'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.front_wheel, self.back_wheel, self.wd_4]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterUnsold(BaseParameter):
    """
    Флаг, отвечающий за показ непроданных авто

    P.S. Если данного флага нет, то недавнопроданные авто также будут в объявлениях
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    unsold = 1
    # Имя
    name = 'unsold'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.unsold]

    def get_dict_parameters(self):
        return {self.name: self.unsold}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterPhoto(BaseParameter):
    """
    Флаг, отвечающий за показ объявлений с авто только с фото

    P.S. Если данный флаг неуставнолен, то будут объявления и без фото
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    photo = 1
    # Имя
    name = 'ph'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.photo]

    def get_dict_parameters(self):
        return {self.name: self.photo}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterFrameAuto(BaseParameter):
    """
    Параметр определяет тип кузова авто.
    Может быть выбрано несколько типов кузова для поиска.
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = True
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    coupe = 1  # Купе
    wagon = 3  # Универсал
    hatchback_3 = 4  # 3х дверный Хэтчбек
    hatchback = 5  # 5 дверный Хэтчбек
    van = 6  # Минивен
    suv = 7  # 5 дверный Джип
    suv_3 = 8  # 3х дверный Джип
    liftback = 9  # Лифтбек
    sedan = 10  # Седан
    open = 11  # Кабриолет, родстер и тарга
    pickup = 12  # Пикап
    # Имя
    name = 'frametype[]'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.coupe, self.wagon, self.hatchback_3, self.hatchback, self.van, self.suv, self.suv_3,
                self.liftback, self.sedan, self.open, self.pickup]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg

    def get_dict_hatchback(self):
        """
        Метод получения словаря, где key = имя параметра; data = список с номерами параметров для 2х Хэтчбеков
        :return: словарь, где key = имя параметра; data = список с номерами параметров для 2х Хэтчбеков
        """
        return {self.name: [self.hatchback_3, self.hatchback]}

    def get_dict_suv(self):
        """
        Метод получения словаря, где key = имя параметра; data = список с номерами параметров для 2х Джипов
        :return: словарь, где key = имя параметра; data = список с номерами параметров для 2х Джипов
        """
        return {self.name: [self.suv_3, self.suv]}


class ParameterColor(BaseParameter):
    """
    Параметр определяет цвет авто.
    Можно выбрать несколько
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = True
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    black = 1  # Черный
    violet = 2  # Фиолетовый
    blue = 3  # Синий
    gray = 4  # Серый
    orange = 5  # Оранжевый
    red = 6  # Красный
    brown = 7  # Коричневый
    golden = 8  # Золотистый
    green = 9  # Зеленый
    yellow = 10  # Желтый
    burgundy = 11  # Бордовый
    white = 12  # Белый
    beige = 13  # Бежевый
    blue_2 = 14  # Голубой
    pink = 15  # Розовый
    silver = 16  # Серебристый
    # Имя
    name = 'colorid[]'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.black, self.violet, self.blue, self.gray, self.orange, self.red, self.brown, self.golden,
                self.green, self.yellow, self.burgundy, self.white, self.beige, self.blue_2, self.pink, self.silver]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterDocument(BaseParameter):
    """
    Параметр фильтрует объявления по состоянию документов
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    problem = 1  # Документов нет или какие-то с ними проблемы
    no_problem = 2  # С документами все в порядке
    # Имя
    name = 'pts'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.problem, self.no_problem]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterDamaged(BaseParameter):
    """
    Пармаетр фильтрует объявления по состоянию авто (требуется ремонт или нет)
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    damaged = 1  # Требуется ремонт
    no_damaged = 2  # Не требуется ремонт
    # Имя
    name = 'damaged'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.damaged, self.no_damaged]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterHandDrive(BaseParameter):
    """
    Параметр фильтрует авто по расположению руля (левый, правый)
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    rhd = 1  # Правый руль
    lhd = 2  # Левый руль
    # Имя
    name = 'w'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.rhd, self.lhd]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMinPower(BaseParameter):
    """
    Параметр позволяет искать объявления с определенной минимальной мощностью авто.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольные
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = True
    # Список со стандартными значениями
    min_power = range(50, 301, 50)
    # Имя
    name = 'minpower'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [*self.min_power]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMaxPower(BaseParameter):
    """
    Параметр позволяет искать объявления с определенной максимальной мощностью авто.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольные
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = True
    # Список со стандартными значениями
    max_power = range(50, 301, 50)
    # Имя
    name = 'maxpower'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [*self.max_power]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMinMileage(BaseParameter):
    """
    Параметр позволяет искать объявления с определенным минимальным пробегом авто.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольные
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = True
    # Список со стандартными значениями
    min_mileage = [1_000, 5_000, 10_000, 20_000, 50_000, 100_000]
    # Имя
    name = 'minprobeg'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return self.min_mileage

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterMaxMileage(BaseParameter):
    """
    Параметр позволяет искать объявления с определенным максимальным пробегом авто.
    Параметр необязательно имеет фиксированные значения, они могут быть произвольные
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = True
    # Список со стандартными значениями
    max_mileage = [1_000, 5_000, 10_000, 20_000, 50_000, 100_000]
    # Имя
    name = 'maxprobeg'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return self.max_mileage

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterOwnerType(BaseParameter):
    """
    Параметр определяет продовца (физ. или юр. лицо)
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    individual = 1  # Физическое лицо (Частник)
    company = 2  # Юридическое лицо (компания)
    # Имя
    name = 'owner_type'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.individual, self.company]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterOwnerSells(BaseParameter):
    """
    Флаг продажи автомобиля от собственника
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    owner = 1  # Собственник
    # Имя
    name = 'OwnerSells'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.name]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterForeign(BaseParameter):
    """
    Флаг, фильтрующий русские автомобили (Только объявления с иномарками)
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    foreign = 1
    # Имя
    name = 'inomarka'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.foreign]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterReport(BaseParameter):
    """
    Флаг показа объявлений, которые имеют отчет ГИБДД по данному авто
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    report = 1
    # Имя
    name = 'vinreport'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.report]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterDromAssist(BaseParameter):
    """
    Флаг показа объявелний, которые прошли проверку ДРОМ-ассистента
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    assist = 1
    # Имя
    name = 'assist'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.assist]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterCert(BaseParameter):
    """
    Флаг показа сертифицированных авто
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    cert = 1
    # Имя
    name = 'cert'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.cert]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterTrade(BaseParameter):
    """
    Флаг, показывающий, что продавец не против совершить обмен авто
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = False
    # Допустимые значения
    trade = 1
    # Имя
    name = 'trade'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return [self.trade]

    def get_dict_parameters(self):
        return {self.name: self.get_list_parameters()}

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg


class ParameterDontMileage(BaseParameter):
    """
    Параметр, позволяющий фильтровать объявления с авто по принципу "без пробега по РФ".
    У него нет никаких параметров, потому что он формируется дополнительным маршрутом, а не как GET-параметр
    """
    # Флаг, который определяет возможность задать несколько аргументов (значений) одновременно
    _f_more_arg = False
    # Флаг, который определяем возможность задавать произвольный аргумент
    _f_arbitrary_arg = True
    # Имя (маршрут)
    name = 'bez-probega'

    def get_name_str(self):
        return self.name

    def get_list_parameters(self):
        return []

    def get_dict_parameters(self):
        return dict()

    def is_more_arg(self):
        return self._f_more_arg

    def is_arbitrary_arg(self):
        return self._f_arbitrary_arg

