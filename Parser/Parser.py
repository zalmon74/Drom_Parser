from bs4 import BeautifulSoup
from bs4.element import Tag as bs4_Tag

from .Headers import HEADERS
from .Functions import get_request, print_sorted_dict_with_separator
from .ConstantsUrls import *
from .Constants import *
from .Errors import Errors


class DromParser:
    """
    Данный класс описывает парсер по Дрому
    """

    def _get_url_city(self, city: str):
        """
        Метод получения ссылки с объявлениями для соответствующего города
        :param city: город
        :return: Сыллка с объявлениями заданного города
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
        """

        try:
            output = self.d_city_href[city]
        except KeyError:
            output = Errors.ERROR_INCORRECT_CITY
        return output

    def _get_url_marque(self, marque: str):
        """
        Метод получения ссылки на описание марки авто
        :param marque: Марка авто
        :return: Ссылка на описание марки авто или
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
        """

        try:
            output = self.d_marque_href[marque]
        except KeyError:
            output = Errors.ERROR_INCORRECT_MARQUE_AUTO
        return output

    def _get_url_model(self, model: str):
        """
        Метод получения ссылки на описание модели авто
        :param model: Модель авто
        :return: Ссылка на описание модели авто или
                 ERROR_INCORRECT_MODEL_AUTO - ОШИБКА: задана несуществующая модель авто
        """

        try:
            output = self.d_model_href[model]
        except KeyError:
            output = Errors.ERROR_INCORRECT_MODEL_AUTO
        return output

    def _set_soup_obj_from_response(self):
        """
        Метод создает soup-объект на основе запроса, если он успешен
        :return:
        """
        if self.response and self.response.ok:
            self.soup_obj = BeautifulSoup(self.response.text, 'html.parser')
        else:
            self.soup_obj = None

    def _set_d_city_href(self):
        """
        Метод заполнения словаря с городами
        """

        # Формируем необходимый запрос
        self.response = get_request(URL_CITIES, HEADERS)
        self.current_url = URL_CITIES
        # Создаем soup-объект
        self._set_soup_obj_from_response()
        # Заполняем словарь с городами и соответствующими URL
        self.d_city_href = self._get_dict_with_city_and_href()

    def _get_dict_with_city_and_href(self) -> dict:
        """
        Метод формирует словарь, который содержит key = Город, data = href - URL с объявлениями этого города
        :return: сформированный словарь
        """

        output_dict = {}
        # Находим на странице теги <noscript>, именно там хранится полный список городов
        list_cities_obj = self.soup_obj.find_all('noscript')
        # Перебираем список и парсим теги
        for city_obj in list_cities_obj:
            # На стринце присутствует объект, который не содержит список городов
            # и внутри он имеет один вложенный объект, поэтому пропускаем именно по этому условию
            if len(city_obj.contents) == 1:
                continue
            else:
                # Итерируемся по вложенным объектам
                for tag in city_obj:
                    # Внутри имеются объекты не относящиеся к тегу, поэтому проверяем,
                    # а потом только добавлям в выходной объект.
                    # Необходимые города храняться только в теге <a>
                    if isinstance(tag, bs4_Tag) and tag.name == 'a':
                        output_dict[tag.text] = tag['href']
        # Чтобы не отдавать пустой словарь. Лучше отдать None
        if len(output_dict) == 0:
            output_dict = None
        return output_dict

    def _set_d_marque_href(self):
        """
        Метод заполнения словаря с марками авто
        """

        # Формируем необходимый запрос
        self.response = get_request(URL_CATALOG, HEADERS)
        self.current_url = URL_CATALOG
        # Создаем soup-объект
        self._set_soup_obj_from_response()
        # Заполняет соответствующий словарь с марками
        self.d_marque_href = self._get_dict_with_marque_and_href()

    def _get_dict_with_marque_and_href(self) -> dict:
        """
        Метод формирует словарь, который содержит key = марка, data = href - URL со всеми доступными моделями авто
        :return: сформированный словарь
        """

        output_dict = {}
        # Сначала парсим по классу 'css-1q61nn e4ojbx42' и получаем популярные марки авто, которые выдаются
        # на главынй экран
        list_marque_obj = self.soup_obj.find_all('div', class_='css-1q61nn e4ojbx42')
        # Итерируемся по маркам и добавляем их в выходной словарь
        for marque_obj in list_marque_obj:
            # Ищем ссылку с параметром data-ftid='component_cars-list-item_hidden-link' и заполняем словарь
            marque_a = marque_obj.find('a', {'data-ftid': 'component_cars-list-item_hidden-link'})
            output_dict[marque_a.text] = marque_a['href']
        # Так как на странице не все марки, то необходимо еще спарсить тэг <noscript> - там располгаются остальная часть
        list_marque_obj = self.soup_obj.find_all('noscript')
        # Перебираем список и парсим теги
        for marque_obj in list_marque_obj:
            # На стринце присутствует объект, который не содержит список марок
            # и внутри он имеет один вложенный объект, поэтому пропускаем именно по этому условию
            if len(marque_obj.contents) == 1:
                continue
            else:
                # Итерируемся по вложенным объектам
                for tag in marque_obj:
                    # Внутри имеются объекты не относящиеся к тегу, поэтому проверяем,
                    # а потом только добавлям в выходной объект.
                    # Необходимые марки храняться только в теге <a>
                    if isinstance(tag, bs4_Tag) and tag.name == 'a':
                        output_dict[tag.text] = tag['href']
        # Чтобы не отдавать пустой словарь. Лучше отдать None
        if len(output_dict) == 0:
            output_dict = None
        return output_dict

    def _set_d_model_href(self, marque: str):
        """
        Метод заполнения словаря с моделями авто
        :param marque: Марка автомобиля, для которой необходимо найти модели
        :return: None - успешное завершения
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
        """

        output = None
        if self.d_marque_href is None:
            self._set_d_marque_href()
        if self.d_marque_href:
            # Проверка на правильность заданной марки
            try:
                url = self.d_marque_href[marque]
            except KeyError:
                output = Errors.ERROR_INCORRECT_MARQUE_AUTO
            else:
                # Формируем запрос
                self.response = get_request(url, HEADERS)
                self.current_url = url
                # Создаем SOUP-объект
                self._set_soup_obj_from_response()
                # Парсим SOUP-объект для получения моделей авто
                self.d_model_href = self._get_dict_with_model_and_href()
                # Задаем выбранную марку автомобиля, если успешно создался словарь с моделями
                if self.d_model_href:
                    self.current_marque = marque
        return output

    def _get_dict_with_model_and_href(self) -> dict:
        """
        Метод формирует словарь, который содержит key = модель, data = href - URL с описанием данной модели
        :return: сформированный словарь
        """

        # Выходной словарь
        output_dict = {}
        # Получаем список доступных моделей, которые хранятся в <div> класса 'css-18clw5c ehmqafe0'
        # Внутри имеется тэг <a>, который хранит ссылка на описание модели с классом 'e64vuai0 css-1i48p5q e104a11t0'
        list_models_obj = self.soup_obj.find_all('a', class_='e64vuai0 css-1i48p5q e104a11t0')
        for model in list_models_obj:
            output_dict[model.text] = model['href']
        return output_dict

    def _set_curr_url(self, city: str = None, marque: str = None, model: str = None):
        """
        Метод устанавливает текущую ссылку с объявлениями в зависимости от входных данных.
        Задать модель без марки автомобиля невзоможно, данный запрос будет откланен
        :param city: Город
        :param marque: Марка автомобиля
        :param model: Модель автомобиля
        :return: None - Успешное выполнение
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
                 ERROR_INCORRECT_MODEL_AUTO - ОШИБКА: задана несуществующая модель авто
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
                 ERROR_MODEL_WITHOUT_MARQUE - ОШИБКА: задана модель без марки авто
        """

        self.current_url = None
        output = None
        # Если не задан ни один параметр, то выдаем все объявления во всех городах
        if city is None and marque is None and model is None:
            output = URL_WITH_ADS_ALL_CITIES
        if model and marque is None:
            output = Errors.ERROR_MODEL_WITHOUT_MARQUE
        # Формируем ссылку на объявления в определенном городе
        if city and marque is None and model is None:
            output = self._get_url_with_ads_for_city(city)
        # Проверяем, что модель задана с маркой
        # Формируем ссылку на объявления по всем городам с определенной маркой авто
        if marque and output is None and city is None and model is None:
            output = self._get_url_with_adds_for_marque(marque)
        # Формируем ссылку на объявления по всем городам с определенной маркой и моделью авто
        if marque and model and output is None and city is None:
            output = self._get_url_with_adds_for_marque_and_model(marque, model)
        # Формируем ссылку на объявления в определеленном городе с определенной маркой машины
        if city and marque and output is None and model is None:
            output = self._get_url_with_adds_for_city_marque(city, marque)
        # Формируем ссылку на объявления в определенном городе с определенной маркой и моделью авто
        if city and marque and model and output is None:
            output = self._get_url_with_adds_for_city_marque_model(city, marque, model)
        # Проверяем, что функция отработала без ошибок и вернула URL, только после этого записываем ее в поле
        if isinstance(output, str):
            self.current_url = output
            output = None
            if marque:
                self.current_marque = marque
            if model:
                self.current_model = model
        else:
            self.current_url = None
        return output

    def _get_url_with_ads_for_city(self, city: str) -> str:
        """
        Метод получения URL с объявлениями для соответствующего города
        :param city: необходимый город
        :return: сформированный адрес или
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
        """

        # Заполняем словарь с городами и ссылками на объявления, если он не заполнен
        if self.d_city_href is None:
            self._set_d_city_href()
        output = self._get_url_city(city)
        return output

    def _get_url_with_adds_for_marque(self, marque: str):
        """
        Метод получения URL с объявлениями для всех городов с соответствующей маркой авто
        :param marque: Марка авто
        :return: Сформированный адрес или
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
        """

        # Заполняем словарь с доступными марками авто, если он не заполнен
        if self.d_marque_href is None:
            self._set_d_marque_href()
        # Получаем ссылку с описанием марки авто
        url_auto = self._get_url_marque(marque)
        # Проверяем, что метод завершился без ошибки. Если так, то вырезаем имя марки из ссылки и вставляем его
        # в общий каталог. Если имеется ошибка, то возвращаем ее
        if isinstance(url_auto, str):
            lst_str = url_auto.split('/')
            # Так как URL заканчивается символом '/', то последний элемент будет пустой, необходимо брать предпослдений
            name_auto = lst_str[-2]
            # Формируем выходной URL
            output = URL_WITH_ADS_ALL_CITIES + f'{name_auto}/'
        else:
            output = url_auto
        return output

    def _get_url_with_adds_for_marque_and_model(self, marque: str, model: str):
        """
        Метод получения URL с объявлениями для всех городов с соответствующей маркой и моделью авто
        :param marque: Марка авто
        :param model: Модель авто
        :return: Сформированный адрес или
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
                 ERROR_INCORRECT_MODEL_AUTO - ОШИБКА: задана несуществующая модель автомобиля
        """

        # Получаем ссылку с объявлениями для марки авто
        url_marque = self._get_url_with_adds_for_marque(marque)
        if isinstance(url_marque, str):
            # Заполняем словарь с доступными моделями, если он не заполнен
            if self.d_model_href is None:
                self._set_d_model_href(marque)
            url_model = self._get_url_model(model)
            # Проверяем, что метод завершился без ошибки. Если так, то вырезаем имя модели из ссылки и вставляем его
            # в общий каталог. Если имеется ошибка, то возвращаем ее
            if isinstance(url_model, str):
                lst_str = url_model.split('/')
                # Так как URL заканчивается символом '/', то последний элемент будет пустой,
                # необходимо брать предпослдений
                model_auto = lst_str[-2]
                # Формируем выходной URL
                output = url_marque + f'{model_auto}/'
            else:
                output = url_model
        else:
            output = url_marque
        return output

    def _get_url_with_adds_for_city_marque(self, city: str, marque: str):
        """
        Метод получения URL с объявлениями для определенного города с соответствующей маркой
        :param city: Город
        :param marque: Марка авто
        :return: Сформированный адрес или
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
        """

        # Получаем адреса с объявлениями для соответствующего города и марки авто по всем городам
        url_city = self._get_url_with_ads_for_city(city)
        if isinstance(url_city, str):
            url_marque = self._get_url_with_adds_for_marque(marque)
            # Проверяем, что метод завершился без ошибки. Если так, то вырезаем имя марки из ссылки и вставляем его
            # в общий каталог. Если имеется ошибка, то возвращаем ее
            if isinstance(url_marque, str):
                lst_str = url_marque.split('/')
                # Так как URL заканчивается символом '/', то последний элемент будет пустой,
                # необходимо брать предпослдений
                name_marque = lst_str[-2]
                output = url_city.replace('auto', name_marque)
            else:
                output = url_marque
        else:
            output = url_city
        return output

    def _get_url_with_adds_for_city_marque_model(self, city: str, marque: str, model: str):
        """
        Метод получения URL c объявленими в определенном городе с определенной маркой и моделью авто
        :param city: Город
        :param marque: Марка авто
        :param model: Модель авто
        :return: Сформированный адрес или
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
                 ERROR_INCORRECT_MODEL_AUTO - ОШИБКА: задана несуществующая модель авто
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
        """

        # Получаем ссылку с объявлениями в определенном городе и соответствующей моделью
        url_city_marque = self._get_url_with_adds_for_city_marque(city, marque)
        if isinstance(url_city_marque, str):
            # Заполняем словарь с доступными моделями, если он не заполнен
            if self.d_model_href is None:
                self._set_d_model_href(marque)
            url_model = self._get_url_model(model)
            # Проверяем, что метод завершился без ошибки. Если так, то вырезаем имя модели из ссылки и вставляем его
            # в общий каталог. Если имеется ошибка, то возвращаем ее
            if isinstance(url_model, str):
                lst_str = url_model.split('/')
                # Так как URL заканчивается символом '/', то последний элемент будет пустой,
                # необходимо брать предпослдений
                model_auto = lst_str[-2]
                # Формируем выходной URL
                output = url_city_marque + f'{model_auto}/'
            else:
                output = url_model
        else:
            output = url_city_marque
        return output

    def __init__(self):
        self.response = None  # Объект с ответом на запрос (последний)
        self.soup_obj = None  # Спарсеный объект (soup) (последний)
        self.d_city_href = None  # Словарь: key = город, data = href - URL с объявлениями этого города
        self.d_marque_href = None  # Словарь: key = марка, data = href - URL со всеми доступными моделями авто
        self.d_model_href = None  # Словарь: key = модель автомобиля, data = href - URL с описанием данной модели
        self.current_url = None  # Текущий URL
        self.current_marque = None  # Выбранная марка автомобиля
        self.current_model = None  # Выбранная модель автомобиля

    def get_available_cities(self) -> list:
        """
        Метод возвращает список доступных городов в ДРОМ
        :return: список доступных городов
        """

        # Если словарь не заполнен, то вызываем метод его заполнения
        if self.d_city_href is None:
            self._set_d_city_href()
        # Формируем выходной объект
        output = None
        if self.d_city_href:
            output = sorted([*self.d_city_href.keys()])
        return output

    def get_available_marques(self) -> list:
        """
        Метод возвращает список доступных марок автомобилей в ДРОМ
        :return: список доступных марок автомобилей
        """

        # Если словарь не заполнен, то вызываем метод его заполнения
        if self.d_marque_href is None:
            self._set_d_marque_href()
        # Формируем выходной объект
        output = None
        if self.d_marque_href:
            output = sorted([*self.d_marque_href.keys()])
        return output

    def get_available_models(self, marque: str) -> list:
        """
        Метод возращает список доступных моделей для соответствующей марки автомобиля
        :param marque: марка автомобиля
        :return: список доступных моделей для соответствующей марки автомобиля
        """

        # Если словарь не заполнен, вызываем метод его заполнения
        error = None
        if self.d_model_href is None:
            error = self._set_d_model_href(marque)
        # Формируем выходной объект
        output = None
        if error is None:
            if self.d_model_href:
                output = sorted([*self.d_model_href.keys()])
        else:
            output = error
        return output

    def get_url_with_ads(self, city: str = None, marque: str = None, model: str = None):
        """
        Метод получения URL с объявлениями с заданными параметрами
        :param city: Город, если None - поиск во всех городах
        :param marque: Марка авто, если None - поиск всех марок
        :param model:  Модель авто, если None - поиск всех моделей (поиск только модели не работает без марки)
        :return: Сформированную ссылку или
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
                 ERROR_INCORRECT_MODEL_AUTO - ОШИБКА: задана несуществующая модель авто
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
                 ERROR_MODEL_WITHOUT_MARQUE - ОШИБКА: задана модель без марки авто
        """

        error = self._set_curr_url(city, marque, model)
        if error is None:
            output = self.current_url
        else:
            output = error
        return output

    # Методы печати

    def print_available_cities(self):
        """
        Метод печати на экран список доступных городов и ссылки на объявления в соот. городе
        """

        # Если словарь не заполнен, то вызываем метод его заполнения
        if self.d_city_href is None:
            self._set_d_city_href()
        # Если словарь сформирован, то просто печает, если нет, то печает на экран ошибку
        if self.d_city_href:
            print_sorted_dict_with_separator(self.d_city_href)
        else:
            print(MASSAGE_ERROR_EMPTY_DICT_CITY_HREF)

    def print_available_marques(self):
        """
        Метод печати на экран список доступных марок и ссылки на список доступных модулей
        """

        # Если словарь не заполнен, то вызываем метод его заполнения
        if self.d_marque_href is None:
            self._set_d_marque_href()
        # Если словарь сформирован, то просто печает, если нет, то печает на экран ошибку
        if self.d_marque_href:
            print_sorted_dict_with_separator(self.d_marque_href)
        else:
            print(MASSAGE_ERROR_EMPTY_DICT_MARQUE_HREF)

    def print_available_models(self, marque: str):
        """
        Метод печати на экран список доступных моделей и ссылки на их описание
        :param marque: марка, модели которой необходимо найти
        """

        # Если словарь не заполнен, вызываем метод его заполнения
        error = None
        if self.d_model_href is None:
            error = self._set_d_model_href(marque)

        if error is None and self.d_model_href:
            print_sorted_dict_with_separator(self.d_model_href)
        else:
            print(f'{MASSAGE_ERROR_INCORRECT_MARQUE_AUTO} ({marque})')
