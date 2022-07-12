import inspect

from bs4 import BeautifulSoup
from bs4.element import Tag as bs4_Tag

import GET_Parameters as GetPar
import Output_Parameters as OutPar
from .Headers import HEADERS
from .Functions import get_request, print_sorted_dict_with_separator
from .ConstantsUrls import *
from .Constants import *
from .Settings import *
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
        # Находим на странице теги ONLY_CITY_TAG_ALL_OBJ_PARAMETER_SETTING, именно там хранится полный список городов
        list_cities_obj = self.soup_obj.find_all(ONLY_CITY_TAG_ALL_OBJ_PARAMETER_SETTING)
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
                    # Необходимые города храняться только в теге ONLY_CITY_TAG_OBJ_PARAMETER_SETTING
                    if isinstance(tag, bs4_Tag) and tag.name == ONLY_CITY_TAG_OBJ_PARAMETER_SETTING:
                        output_dict[tag.text] = tag[ONLY_CITY_LINK_PARAMETER_SETTING_SETTING]
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
        # Сначала парсим по классу MARQUE_POPULAR_CLASS_CSS_OBJ_PARAMETER_SETTING и получаем популярные марки авто,
        # которые выдаются на главынй экран
        list_marque_obj = self.soup_obj.find_all(MARQUE_POPULAR_TAG_OBJ_PARAMETER_SETTING,
                                                 class_=MARQUE_POPULAR_CLASS_CSS_OBJ_PARAMETER_SETTING)
        # Итерируемся по маркам и добавляем их в выходной словарь
        for marque_obj in list_marque_obj:
            # Ищем ссылку с параметром NAME_OBJ_MARQUE_PARAMETER_SETTING=DATA_OBJ_MARQUE_PARAMETER_SETTING
            # и заполняем словарь
            marque_a = marque_obj.find(MARQUE_TAG_OBJ_PARAMETER_SETTING,
                                       {MARQUE_NAME_OBJ_PARAMETER_SETTING: MARQUE_DATA_OBJ_PARAMETER_SETTING})
            output_dict[marque_a.text] = marque_a[MARQUE_LINK_PARAMETER_SETTING]
        # Так как на странице не все марки, то необходимо еще спарсить тэг TAG_ALL_OBJ_MAQUE_PARAMETER_SETTING -
        # там располгаются остальная часть
        list_marque_obj = self.soup_obj.find_all(MARQUE_TAG_ALL_OBJ_PARAMETER_SETTING)
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
                    if isinstance(tag, bs4_Tag) and tag.name == MARQUE_TAG_OBJ_PARAMETER_SETTING:
                        output_dict[tag.text] = tag[MARQUE_LINK_PARAMETER_SETTING]
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
        # Внутри имеется тэг MODEL_TAG_ALL_OBJ_PARAMETER_SETTING, который хранит ссылка на описание модели с классом
        # MODEL_CLASS_CSS_OBJ_PARAMETER_SETTING
        list_models_obj = self.soup_obj.find_all(MODEL_TAG_ALL_OBJ_PARAMETER_SETTING,
                                                 class_=MODEL_CLASS_CSS_OBJ_PARAMETER_SETTING)
        for model in list_models_obj:
            output_dict[model.text] = model[MODE_LINK_PARAMETER_SETTING]
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
                # необходимо брать предпоследний
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
                # необходимо брать предпоследний
                name_marque = lst_str[-2]
                output = url_city.replace(NAME_AUTO_URL_PARAMETER_SETTING, name_marque)
            else:
                output = url_marque
        else:
            output = url_city
        return output

    def _get_url_with_adds_for_city_marque_model(self, city: str, marque: str, model: str):
        """
        Метод получения URL c объявлениями в определенном городе с определенной маркой и моделью авто
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

    def _set_list_available_get_parameters(self):
        """
        Метод формирует список с доступными объектами get-параметров для запроса
        """
        # Определяем какие существуют get-параметры
        l_parameters = inspect.getmembers(GetPar, inspect.isclass)
        # Оставляем только их объекты
        self._l_available_get_parameters = list()
        for name, obj in l_parameters:
            self._l_available_get_parameters.append(obj)
        # Убираем вспомогательные объекты типа базового класса и тп.
        self._l_available_get_parameters.remove(GetPar.BaseParameter)
        self._l_available_get_parameters.remove(GetPar.datetime)

    def _add_getparameter(self, parameter: GetPar.BaseParameter, value: int | list):
        """
        Метод добавляет GET-параметр в словарь
        :param parameter: Объект параметра, который необходимо добавить в запрос
        :param value: значение или значения, которые содержит данный параметр
        :return: None - успешное выполнение
                 ERROR_INCORRECT_ARGUMENT_FOR_GET_PARAMETER - ОШИБКА: Данный параметр не может иметь такой аргумент
        """
        output = None
        if value in parameter.get_list_parameters() or parameter.is_arbitrary_arg():
            self.d_parameters[parameter.get_name_str()] = value
        else:
            output = Errors.ERROR_INCORRECT_ARGUMENT_FOR_GET_PARAMETER
        return output

    def _add_parameter_dont_mileage(self):
        """
        Метод добавления к существующему URL маршрут для параметра 'Без-пробега'
        """
        # Проверяем, что данный параметр задан
        try:
            self.d_parameters[GetPar.DONT_MILEAGE_PARAMETER.get_name_str()]
        except KeyError:
            pass
        else:
            if isinstance(self.current_url, str):
                self.current_url += GetPar.DONT_MILEAGE_PARAMETER.get_name_str() + '/'

    def _get_dict_with_parse_soup_obj_for_1_obj(self, input_obj: bs4_Tag) -> dict:
        """
        Метод получения словаря с парсенным SOUP-объектом.
        :param input_obj: Тэг (объект), который необходимо спарсить
        :return: Словарь, где key = Название объявления, data = словарь с различными параметрами:
                                                         {NAME_URL_OUTPUT_PARAMETER: 'Страница с самим объявлением'}
                                                         {NAME_PRICE_OUTPUT_PARAMETER: Цена авто}
                                                         {NAME_DESC_PRICE_OUTPUT_PARAMETER: 'Описание цены'}
                                                         {NAME_CITY_PRICE_OUTPUT_PARAMETER: 'Город'}
                                                         {NAME_DATE_OUTPUT_PARAMETER: 'Дата подачи объявления'}
                                                         {NAME_DESCRIPTION_OUTPUT_PARAMETER: 'Описание авто'}
                                                         {NAME_PHOTO_OUTPUT_PARAMETERS: [URL на фото]}
                                                         {NAME_ENGINE_OUTPUT_PARAMETERS: 'Описание двигателя'}
                                                         {NAME_POWER_OUTPUT_PARAMETERS: Кол-во Л.С.}
                                                         {NAME_TRANSMISSION_OUTPUT_PARAMETERS: 'Коробка передач'}
                                                         {NAME_COLOR_OUTPUT_PARAMETERS: 'Цвет'}
                                                         {NAME_MILEAGE_OUTPUT_PARAMETER: Пробег автомобиля}
                                                         {NAME_HAND_DRIVE_OUTPUT_PARAMETER: 'Расположение руля'}
        """
        # Словарь с параметрами, которые указаны в выходных флагах
        data_output = dict()
        # Определяем название объявления
        title = input_obj.find(TITLE_TAG_OBJ_PARAMETER_SETTING,
                               {TITLE_NAME_OBJ_PARAMETER_SETTING: TITLE_DATA_OBJ_PARAMETER_SETTING}).text
        # Определяем URL объявления
        url = input_obj[ADS_LINK_PARAMETER_SETTING]
        # Проверяем URL и парсим страницу с объявлением
        response_obj = get_request(url, headers=HEADERS)
        # Получаем soup-объект объявления
        if response_obj and response_obj.ok:
            soup_obj_ads = BeautifulSoup(response_obj.text, 'html.parser')
            # Получаем описание авто
            try:
                description = soup_obj_ads.find(FULL_DESCRIPTION_TAG_OBJ_PARAMETER_SETTING,
                                                class_=FULL_DESCRIPTION_CLASS_CSS_OBJ_PARAMETER_SETTING)
                description = description.find(DESCRIPTION_TAG_OBJ_PARAMETER_SETTING,
                                               class_=DESCRIPTION_CLASS_CSS_OBJ_PARAMETER_SETTING).text
            except AttributeError:
                description = MESSAGE_OUTPUT_DESCRIPTION
            # Получаем ссылки на фото
            photos = []
            try:
                lst_obj_photos = soup_obj_ads.find(PHOTO_TAG_ALL_OBJ_PARAMETER_SETTING,
                                                   {PHOTO_NAME_OBJ_PARAMETER_SETTING: PHOTO_DATA_OBJ_PARAMETER_SETTING}
                                                   ).find_all(PHOTO_TAG_OBJ_PARAMETER_SETTING)
                for obj_photo in lst_obj_photos:
                    if isinstance(obj_photo, bs4_Tag) and obj_photo.name == PHOTO_TAG_OBJ_PARAMETER_SETTING:
                        photos.append(obj_photo[PHOTO_LINK_PARAMETER_SETTING])
            except AttributeError:
                photos = MESSAGE_OUTPUT_PHOTOS
            # Описание двигателя
            try:
                engine = soup_obj_ads.find(ENGINE_TAG_OBJ_PARAMETER_SETTING,
                                           text=ENGINE_TEXT_PARAMETER_SETTING).next_sibling.next_sibling.text
            except AttributeError:
                engine = MESSAGE_OUTPUT_ENGINE
            # Мощность
            try:
                power = int(soup_obj_ads.find(POWER_TAG_OBJ_PARAMETER_SETTING,
                                              text=POWER_TEXT_PARAMETER_SETTING).next_sibling.text.split()[0])
            except AttributeError:
                power = MESSAGE_OUTPUT_POWER
            # Коробка передач
            try:
                transmission = soup_obj_ads.find(TRANSMISSION_TAG_OBJ_PARAMETER_SETTING,
                                                 text=TRANSMISSION_TEXT_PARAMETER_SETTING).next_sibling.text
            except AttributeError:
                transmission = MESSAGE_OUTPUT_TRANSMISSION
            # Цвет
            try:
                color = soup_obj_ads.find(COLOR_TAG_OBJ_PARAMETER_SETTING,
                                          text=COLOR_TEXT_PARAMETER_SETTING).next_sibling.text
            except AttributeError:
                color = MESSAGE_OUTPUT_COLOR
            # Пробег
            try:
                mileage = soup_obj_ads.find(MILEAGE_TAG_OBJ_PARAMETER_SETTING,
                                            text=MILEAGE_TEXT_PARAMETER_SETTING).next_sibling.text.split()[0]
                mileage = mileage.split(',')[0]
                # Избовляемся от Юникода
                print(title)
                mileage = mileage.encode('ascii', 'ignore')
                mileage = int(mileage.decode())
            except AttributeError:
                mileage = MESSAGE_OUTPUT_MILEAGE
            # Расположение руля
            try:
                hand_drive = soup_obj_ads.find(HAND_DRIVE_TAG_OBJ_PARAMETER_SETTING,
                                               text=HAND_DRIVE_TEXT_PARAMETER_SETTING).next_sibling.text
            except AttributeError:
                hand_drive = MESSAGE_OUTPUT_HAND_DRIVE
        else:
            description = MESSAGE_OUTPUT_DESCRIPTION
            photos = MESSAGE_OUTPUT_PHOTOS
            engine = MESSAGE_OUTPUT_ENGINE
            power = MESSAGE_OUTPUT_POWER
            transmission = MESSAGE_OUTPUT_TRANSMISSION
            color = MESSAGE_OUTPUT_COLOR
            mileage = MESSAGE_OUTPUT_MILEAGE
            hand_drive = MESSAGE_OUTPUT_HAND_DRIVE
        # Определяем цену авто
        price = input_obj.find(PRICE_TAG_OBJ_PARAMETER_SETTING,
                               {PRICE_NAME_OBJ_PARAMETER_SETTING: PRICE_DATA_OBJ_PARAMETER_SETTING}).text
        # Избовляемся от Юникода
        price = price.encode('ascii', 'ignore')
        price = int(price.decode())
        # Определяем описание цены
        try:
            desc_price = input_obj.find(DESC_PRICE_TAG_OBJ_PARAMETER_SETTING,
                                        class_=DESC_PRICE_CLASS_CSS_OBJ_PARAMETER_SETTING).text
        except AttributeError:
            desc_price = MESSAGE_OUTPUT_DESC_PRICE
        # Определяем город авто
        city = input_obj.find(CITY_TAG_OBJ_PARAMETER_SETTING, class_=CITY_CLASS_CSS_OBJ_PARAMETER_SETTING).text
        # Определяем дату объявления
        date = input_obj.find(DATE_TAG_OBJ_PARAMETER_SETTING,
                              {DATE_NAME_OBJ_PARAMETER_SETTING: DATE_DATA_OBJ_PARAMETER_SETTING}).text

        # Добавляем полученные данные в выходной словарь
        if self._l_output_parameters[OutPar.IND_URL_OUTPUT_PARAMETER]:
            data_output[OutPar.NAME_URL_OUTPUT_PARAMETER] = url
        if self._l_output_parameters[OutPar.IND_PRICE_OUTPUT_PARAMETER]:
            data_output[OutPar.NAME_PRICE_OUTPUT_PARAMETER] = price
        if self._l_output_parameters[OutPar.IND_DESC_PRICE_OUTPUT_PARAMETER]:
            data_output[OutPar.NAME_DESC_PRICE_OUTPUT_PARAMETER] = desc_price
        if self._l_output_parameters[OutPar.IND_CITY_PRICE_OUTPUT_PARAMETER]:
            data_output[OutPar.NAME_CITY_PRICE_OUTPUT_PARAMETER] = city
        if self._l_output_parameters[OutPar.IND_DATE_OUTPUT_PARAMETER]:
            data_output[OutPar.NAME_DATE_OUTPUT_PARAMETER] = date
        if self._l_output_parameters[OutPar.IND_PHOTO_OUTPUT_PARAMETERS]:
            data_output[OutPar.NAME_DESCRIPTION_OUTPUT_PARAMETER] = photos
        if self._l_output_parameters[OutPar.IND_DESCRIPTION_OUTPUT_PARAMETER]:
            data_output[OutPar.NAME_DESCRIPTION_OUTPUT_PARAMETER] = description
        if self._l_output_parameters[OutPar.IND_PHOTO_OUTPUT_PARAMETERS]:
            data_output[OutPar.NAME_PHOTO_OUTPUT_PARAMETERS] = photos
        if self._l_output_parameters[OutPar.IND_ENGINE_OUTPUT_PARAMETERS]:
            data_output[OutPar.NAME_ENGINE_OUTPUT_PARAMETERS] = engine
        if self._l_output_parameters[OutPar.IND_POWER_OUTPUT_PARAMETERS]:
            data_output[OutPar.NAME_POWER_OUTPUT_PARAMETERS] = power
        if self._l_output_parameters[OutPar.IND_TRANSMISSION_OUTPUT_PARAMETERS]:
            data_output[OutPar.NAME_TRANSMISSION_OUTPUT_PARAMETERS] = transmission
        if self._l_output_parameters[OutPar.IND_COLOR_OUTPUT_PARAMETERS]:
            data_output[OutPar.NAME_COLOR_OUTPUT_PARAMETERS] = color
        if self._l_output_parameters[OutPar.IND_MILEAGE_OUTPUT_PARAMETER]:
            data_output[OutPar.NAME_MILEAGE_OUTPUT_PARAMETER] = mileage
        if self._l_output_parameters[OutPar.IND_HAND_DRIVE_OUTPUT_PARAMETER]:
            data_output[OutPar.NAME_HAND_DRIVE_OUTPUT_PARAMETER] = hand_drive

        output = {title: data_output}
        return output

    def _get_dict_with_parse_soup_obj_for_1_page(self) -> dict:
        """
        Метод получения словаря с парсенным SOUP-объектов для одной страницы.
        :return: None - Если на данной странице нет объявлений
                 Словарь, где key = Номер объявление на странице, data = словарь, где
                                                    key = Название объявления, data = словарь с различными параметрами:
                                                    {NAME_URL_OUTPUT_PARAMETER: 'Страница с самим объявлением'}
                                                    {NAME_PRICE_OUTPUT_PARAMETER: Цена авто}
                                                    {NAME_DESC_PRICE_OUTPUT_PARAMETER: 'Описание цены'}
                                                    {NAME_CITY_PRICE_OUTPUT_PARAMETER: 'Город'}
                                                    {NAME_DATE_OUTPUT_PARAMETER: 'Дата подачи объявления'}
                                                    {NAME_DESCRIPTION_OUTPUT_PARAMETER: 'Описание авто'}
                                                    {NAME_PHOTO_OUTPUT_PARAMETERS: [URL на фото]}
                                                    {NAME_ENGINE_OUTPUT_PARAMETERS: 'Описание двигателя'}
                                                    {NAME_POWER_OUTPUT_PARAMETERS: Кол-во Л.С.}
                                                    {NAME_TRANSMISSION_OUTPUT_PARAMETERS: 'Коробка передач'}
                                                    {NAME_COLOR_OUTPUT_PARAMETERS: 'Цвет'}
                                                    {NAME_MILEAGE_OUTPUT_PARAMETER: Пробег автомобиля}
                                                    {NAME_HAND_DRIVE_OUTPUT_PARAMETER: 'Расположение руля'}
        """
        output = None
        # Каждое объявление имеет css class = ADS_CLASS_CSS_OBJ_PARAMETER_SETTING По нему и будем фильтровать данные
        # на странице
        l_ads = self.soup_obj.find_all(ADS_TAG_OBJ_PARAMETER_SETTING, class_=ADS_CLASS_CSS_OBJ_PARAMETER_SETTING)
        if l_ads:
            output = dict()
        num_ads = 0
        # Перебираем все объявления и заполняем выходной словарь
        for obj_ads in l_ads:
            output_1_obj = self._get_dict_with_parse_soup_obj_for_1_obj(obj_ads)
            output[num_ads] = output_1_obj
            num_ads += 1
        return output

    def _next_page_ads(self, next_num_page: int):
        """
        Метод установки URL со следующей страницы пагинации объявлений
        :param next_num_page: номер следующей страницы
        """
        url = self.current_url
        # Если мы находимся на первой странице, то в ее URL отсутствует маршрут типа 'page' соответственно нужно его
        # добавить. Он находится в [-2] при разбиении URL. Иначе, просто изменить соответствующий номер страницы
        split_url = url.split('/')
        if 'page' in split_url[-2]:
            split_url[-2] = f'page{next_num_page}'
        else:
            split_url.insert(-1, f'page{next_num_page}')
        self.current_url = '/'.join(split_url)

    def _set_dict_with_parse_ads(self, city: str = None, marque: str = None, model: str = None,
                                 f_with_params: bool = False, step_num_page: int = 1):
        """
        Метод формирования словаря со всеми спарсенными объявлениями с заданными условиями.
        Полученный словарь кладет в соответствующее поле

        :param city: Город, если None - поиск во всех городах
        :param marque: Марка авто, если None - поиск всех марок
        :param model: Модель авто, если None - поиск всех моделей (поиск только модели не работает без марки)
        :param f_with_params: Флаг запроса с GET-параметрами, которые ранее были установлены
                              True = с параметрами, False = без параметров
        :param step_num_page: Шаг по страницам объявлений

        :return: None - успешное выполнение или
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
                 ERROR_INCORRECT_MODEL_AUTO - ОШИБКА: задана несуществующая модель авто
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
                 ERROR_MODEL_WITHOUT_MARQUE - ОШИБКА: задана модель без марки авто
        """
        output = None
        # Получаем ссылку с объявлениями
        error = self._set_curr_url(city, marque, model)
        if error is None:
            # Формируем словарь
            dict_ads = dict()
            # Бесконечный цикл для парсинга каждой страницы, как только на странице не окажется объявлений, то
            # он завершится
            num_page = 0
            while True:
                if f_with_params and num_page == 0:
                    # Добавляем особый параметр "Без пробега", если он задан и формируем запрос
                    self._add_parameter_dont_mileage()
                    self.response = get_request(self.current_url, HEADERS, self.d_parameters)
                    self.current_url = self.response.url
                else:
                    self.response = get_request(self.current_url, HEADERS)
                    self.current_url = self.response.url
                # Формируем soup-объект
                self._set_soup_obj_from_response()
                # Парсим одну страницу
                dict_one_page = self._get_dict_with_parse_soup_obj_for_1_page()
                if dict_one_page is None:
                    break
                else:
                    dict_ads[num_page] = dict_one_page
                    # Переходим на следующую страницу
                    num_page += step_num_page
                    self._next_page_ads(num_page+1)
            # Полсе парсинга всех страниц заполняем поле
            self.d_parse_ads = dict_ads
        else:
            output = error
        return output

    def __init__(self):
        # Список с доступными объектами get-параметров для запроса
        self._l_available_get_parameters = None
        # Список с флагами для выходных параметров
        # [IND_URL_OUTPUT_PARAMETER] = url
        # [IND_PRICE_OUTPUT_PARAMETER] = price
        # [IND_DESC_PRICE_OUTPUT_PARAMETER] = desc_price
        # [IND_CITY_PRICE_OUTPUT_PARAMETER] = city
        # [IND_DATE_OUTPUT_PARAMETER] = date
        # [IND_DESCRIPTION_OUTPUT_PARAMETER] = description
        # [IND_PHOTO_OUTPUT_PARAMETERS] = photo
        # [IND_ENGINE_OUTPUT_PARAMETERS] = engine
        # [IND_POWER_OUTPUT_PARAMETERS] = power
        # [IND_TRANSMISSION_OUTPUT_PARAMETERS] = transmission
        # [IND_COLOR_OUTPUT_PARAMETERS] = color
        # [IND_MILEAGE_OUTPUT_PARAMETER] = mileage
        # [IND_HAND_DRIVE_OUTPUT_PARAMETER] = hand_drive
        self._l_output_parameters = [True for _ in range(13)]

        self.response = None  # Объект с ответом на запрос (последний)
        self.soup_obj = None  # Спарсеный объект (soup) (последний)
        self.d_city_href = None  # Словарь: key = город, data = href - URL с объявлениями этого города
        self.d_marque_href = None  # Словарь: key = марка, data = href - URL со всеми доступными моделями авто
        self.d_model_href = None  # Словарь: key = модель автомобиля, data = href - URL с описанием данной модели
        self.d_parse_ads = None  # Словарь: key = номер страницы, data = словарь с парсенными данными
        self.d_parameters = dict()  # Словарь с доп. параметрами: key = имя параметра, data = значение или значения
        self.current_url = None  # Текущий URL
        self.current_marque = None  # Выбранная марка автомобиля
        self.current_model = None  # Выбранная модель автомобиля

        # Заполняем список с get-параметрами для запросов
        self._set_list_available_get_parameters()

    # Геттеры

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
        Метод возвращает список доступных моделей для соответствующей марки автомобиля
        :param marque: марка автомобиля
        :return: список доступных моделей для соответствующей марки автомобиля
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
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

    def get_url_with_ads(self, city: str = None, marque: str = None, model: str = None, f_with_params: bool = False):
        """
        Метод получения URL с объявлениями с заданными параметрами
        :param city: Город, если None - поиск во всех городах
        :param marque: Марка авто, если None - поиск всех марок
        :param model:  Модель авто, если None - поиск всех моделей (поиск только модели не работает без марки)
        :param f_with_params: Флаг запроса с GET-параметрами, которые ранее были установлены
                              True = с параметрами, False = без параметров
        :return: Сформированную ссылку или
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
                 ERROR_INCORRECT_MODEL_AUTO - ОШИБКА: задана несуществующая модель авто
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
                 ERROR_MODEL_WITHOUT_MARQUE - ОШИБКА: задана модель без марки авто
        """
        error = self._set_curr_url(city, marque, model)
        if error is None:
            if f_with_params:
                # Добавляем особый параметр "Без пробега", если он задан и формируем запрос
                self._add_parameter_dont_mileage()
                response = get_request(self.current_url, HEADERS, self.d_parameters)
                if response.ok:
                    self.current_url = response.url
            output = self.current_url
        else:
            output = error
        return output

    def get_dict_with_parse_ads(self, city: str = None, marque: str = None, model: str = None,
                                f_with_params: bool = False, step_num_page: int = 1):
        """
        Метод получения словаря с парсенными объявлениями
        :param city: Город, если не задан - поиск по всем городам
        :param marque: Марка авто, если на задана - поиск по всем городам
        :param model: Модель авто, если на задана - поиск по всем городам
        :param f_with_params: Флаг поиска с дополнительными GET-параметрами (различные фильтры объявлений)
        :param step_num_page: Шаг по страницам с объявлений
                              step_num_page: Шаг по страницам объявлений
        :return: Словарь, где key = номер страницы объявления, а data = Словарь
                                        Словарь, где key = Номер объявление на странице, data = словарь, где
                                                    key = Название объявления, data = словарь с различными параметрами:
                                                    {NAME_URL_OUTPUT_PARAMETER: 'Страница с самим объявлением'}
                                                    {NAME_PRICE_OUTPUT_PARAMETER: Цена авто}
                                                    {NAME_DESC_PRICE_OUTPUT_PARAMETER: 'Описание цены'}
                                                    {NAME_CITY_PRICE_OUTPUT_PARAMETER: 'Город'}
                                                    {NAME_DATE_OUTPUT_PARAMETER: 'Дата подачи объявления'}
                                                    {NAME_DESCRIPTION_OUTPUT_PARAMETER: 'Описание авто'}
                                                    {NAME_PHOTO_OUTPUT_PARAMETERS: [URL на фото]}
                                                    {NAME_ENGINE_OUTPUT_PARAMETERS: 'Описание двигателя'}
                                                    {NAME_POWER_OUTPUT_PARAMETERS: Кол-во Л.С.}
                                                    {NAME_TRANSMISSION_OUTPUT_PARAMETERS: 'Коробка передач'}
                                                    {NAME_COLOR_OUTPUT_PARAMETERS: 'Цвет'}
                                                    {NAME_MILEAGE_OUTPUT_PARAMETER: Пробег автомобиля}
                                                    {NAME_HAND_DRIVE_OUTPUT_PARAMETER: 'Расположение руля'}
                 ERROR_INCORRECT_MARQUE_AUTO - ОШИБКА: задана несуществующая марка автомобиля
                 ERROR_INCORRECT_MODEL_AUTO - ОШИБКА: задана несуществующая модель авто
                 ERROR_INCORRECT_CITY - ОШИБКА: задан несуществующий город
                 ERROR_MODEL_WITHOUT_MARQUE - ОШИБКА: задана модель без марки авто
        """
        output = self._set_dict_with_parse_ads(city, marque, model, f_with_params, step_num_page)
        if output is None and len(self.d_parse_ads) != 0:
            output = self.d_parse_ads
        return output

    # Сеттеры

    def set_getparameter(self, parameter: GetPar.BaseParameter | GetPar.ParameterDontMileage, value: int | list):
        """
        Метод добавления (установки) get-параметра для запроса
        :param parameter: Объект параметра, который необходимо добавить в запрос
        :param value: значение или значения, которые содержит данный параметр
        :return: None - успешное завершение
                 ERROR_INCORRECT_GET_PARAMETER - ОШИБКА: Заданный параметр отсутствует или недоступен
                 ERROR_INCORRECT_COUNT_ARG_FOR_GET_PARAMETER - ОШИБКА: Данный параметр может иметь только один арг.
                 ERROR_INCORRECT_ARGUMENT_FOR_GET_PARAMETER - ОШИБКА: Данный параметр не может иметь такой аргумент
        """
        output = None
        # Проверяем наличие заданного параметра
        if type(parameter) in self._l_available_get_parameters:
            # Проверяем соответствие аргументов для данного параметра
            if isinstance(value, list) and parameter.is_more_arg():
                for val in value:
                    output = self._add_getparameter(parameter, val)
                    if output:
                        break
            elif isinstance(value, int):
                output = self._add_getparameter(parameter, value)
            else:  # Данный параметр может иметь только один аргумент
                output = Errors.ERROR_INCORRECT_COUNT_ARG_FOR_GET_PARAMETER
        else:  # Заданного параметра нет, или он не доступен
            output = Errors.ERROR_INCORRECT_GET_PARAMETER
        return output

    def set_output_parameters(self, *args, f_url: bool = True, f_price: bool = True, f_desc_price: bool = True,
                              f_city: bool = True, f_date: bool = True, f_description: bool = True,
                              f_photo: bool = True, f_engine: bool = True, f_power: bool = True,
                              f_transmission: bool = True, f_color: bool = True, f_mileage: bool = True,
                              f_hand_drive: bool = True):
        """
        Метод установки флагов выходных параметров. По умолчанию все флаги установлены в True.
        Можно задать сразу списком параметров, индексы которых указаны ниже в качестве первого аргумента.
        :param f_url: флаг выдачи URL на соответствующее объявление
        :param f_price: флаг выдачи цены данного объявления
        :param f_desc_price: флаг выдачи описания цены, с точки зрения, ДРОМа
        :param f_city: флаг выдачи города, в которой продается соответствующее автомобиля
        :param f_date: флаг выдачи даты размещения объявления
        :param f_description: флаг выдачи описания объявления
        :param f_photo: флаг выдачи URL на фото с объявления
        :param f_engine: флаг выдачи описания двигателя автомобиля
        :param f_power: флаг выдачи мощности автомобиля
        :param f_transmission: флаг выдачи коробки передач автомобиля
        :param f_color: флаг выдачи цвета автомобиля
        :param f_mileage: флаг выдачи пробега автомобиля
        :param f_hand_drive: флаг выдачи расположения руля автомобиля
        :param args[0]: Список с белевыми значениями, который позволяет задать вектор с флагами выходных параметров
                        сразу, а не по одному соответствующему параметру. Расположение параметров в векторе следующее:
                        [IND_URL_OUTPUT_PARAMETER] = url
                        [IND_PRICE_OUTPUT_PARAMETER] = price
                        [IND_DESC_PRICE_OUTPUT_PARAMETER] = desc_price
                        [IND_CITY_PRICE_OUTPUT_PARAMETER] = city
                        [IND_DATE_OUTPUT_PARAMETER] = date
                        [IND_DESCRIPTION_OUTPUT_PARAMETER] = description
                        [IND_PHOTO_OUTPUT_PARAMETERS] = photo
                        [IND_ENGINE_OUTPUT_PARAMETERS] = engine
                        [IND_POWER_OUTPUT_PARAMETERS] = power
                        [IND_TRANSMISSION_OUTPUT_PARAMETERS] = transmission
                        [IND_COLOR_OUTPUT_PARAMETERS] = color
                        [IND_MILEAGE_OUTPUT_PARAMETER] = mileage
                        [IND_HAND_DRIVE_OUTPUT_PARAMETER] = hand_drive
        """
        if len(args) == 0:
            self._l_output_parameters = [True for _ in range(13)]
            self._l_output_parameters[OutPar.IND_URL_OUTPUT_PARAMETER] = f_url
            self._l_output_parameters[OutPar.IND_HAND_DRIVE_OUTPUT_PARAMETER] = f_hand_drive
            self._l_output_parameters[OutPar.IND_COLOR_OUTPUT_PARAMETERS] = f_color
            self._l_output_parameters[OutPar.IND_DATE_OUTPUT_PARAMETER] = f_date
            self._l_output_parameters[OutPar.IND_DESCRIPTION_OUTPUT_PARAMETER] = f_description
            self._l_output_parameters[OutPar.IND_CITY_PRICE_OUTPUT_PARAMETER] = f_city
            self._l_output_parameters[OutPar.IND_DESC_PRICE_OUTPUT_PARAMETER] = f_desc_price
            self._l_output_parameters[OutPar.IND_ENGINE_OUTPUT_PARAMETERS] = f_engine
            self._l_output_parameters[OutPar.IND_MILEAGE_OUTPUT_PARAMETER] = f_mileage
            self._l_output_parameters[OutPar.IND_PHOTO_OUTPUT_PARAMETERS] = f_photo
            self._l_output_parameters[OutPar.IND_POWER_OUTPUT_PARAMETERS] = f_power
            self._l_output_parameters[OutPar.IND_PRICE_OUTPUT_PARAMETER] = f_price
            self._l_output_parameters[OutPar.IND_TRANSMISSION_OUTPUT_PARAMETERS] = f_transmission
        elif len(args[0]) == 13:
            self._l_output_parameters = args[0]

    # Методы отчистки

    def clear_getparameters(self):
        """
        Метод очистки словаря с GET-параметрами
        """
        self.d_parameters.clear()

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
