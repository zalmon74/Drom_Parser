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
                 ERROR_MARQUE_AUTO - заданной марки автомобиля нет
        """

        output = None
        if self.d_marque_href is None:
            self._set_d_marque_href()
        if self.d_marque_href:
            # Проверка на правильность заданной марки
            try:
                url = self.d_marque_href[marque]
            except KeyError:
                output = Errors.ERROR_MARQUE_AUTO
            else:
                # Формируем запрос
                self.response = get_request(url, HEADERS)
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

    def __init__(self):
        self.response = None  # Объект с ответом на запрос (последний)
        self.soup_obj = None  # Спарсеный объект (soup) (последний)
        self.d_city_href = None  # Словарь: key = город, data = href - URL с объявлениями этого города
        self.d_marque_href = None  # Словарь: key = марка, data = href - URL со всеми доступными моделями авто
        self.d_model_href = None  # Словарь: key = модель автомобиля, data = href - URL с описанием данной модели
        self.current_marque = None  # Выбранная марка автомобиля

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
