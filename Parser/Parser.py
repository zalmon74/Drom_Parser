from bs4 import BeautifulSoup
from bs4.element import Tag as bs4_Tag

from .Headers import HEADERS
from .Functions import get_request
from .ConstantsUrls import *
from .Constants import *


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

    def __init__(self):
        self.response = None  # Объект с ответом на запрос (последний)
        self.soup_obj = None  # Спарсеный объект (soup) (последний)
        self.d_city_href = None  # Словарь: key = город, data = href - URL с объявлениями этого города

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
            output = [*self.d_city_href.keys()]
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
            for city, href in self.d_city_href.items():
                print(f"{city} | {href}")
        else:
            print(MASSAGE_ERROR_EMPTY_DICT_CITY_HREF)
