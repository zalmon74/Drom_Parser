from pathlib import Path
import sys

# Добавляем в путь сбора модуль с параметрами
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))


import json
import csv
from os import system

import CLI_Settings.Main_Menu_Settings as MainMenuSett
import CLI_Settings.Get_List_Parameters_Menu_Settings as GetListMenuSett
import CLI_Settings.Set_List_Parameters_Menu_Settings as SetListMenuSett
import CLI_Settings.Output_List_Parameters_Menu_Settings as OutListMenuSett
import CLI_Settings.GETParameters_Menu_Settings as GetParMenuSett
import CLI_Settings.Messages as Mess
import Menu
import Parser

from .Functions import input_unsigned_int


class CLIDromParser:
    """ CLI для парсера дрома """

    def _create_menu_with_cities(self):
        """ Метод создания меню с выбором города """
        l_cities = self._parser.get_available_cities()
        for city in l_cities:
            self._cities_menu.add_field(city)

    def _create_menu_with_marques(self):
        """ Метод создания меню с выбором марки авто """
        l_marques = self._parser.get_available_marques()
        for marque in l_marques:
            self._marques_menu.add_field(marque)

    def _create_menu_with_models(self, marque: str):
        """
        Метод создания меню с выбором модели авто

        :param marque: имя марки авто
        """
        l_models = self._parser.get_available_models(marque)
        for model in l_models:
            self._marques_menu.add_field(model)

    def _control_main_menu(self):
        """ Метод управления главным меню """
        # Запускаем главное меню
        while True:
            result = self._main_menu.start()
            if result == MainMenuSett.FIELD_GET_LIST_PARAMETERS_MAIN_MENU:
                # Запускаем меню с установкой параметров через меню
                result = self._control_get_list_menu()
            if result == MainMenuSett.FIELD_SET_LIST_PARAMETERS_MAIN_MENU:
                # Запускаем меню с установкой параметров
                result = self._control_set_list_menu()
            if result == MainMenuSett.FIELD_START_PARSER_RESULT_SAVE_JSON_MAIN_MENU:
                # Запускаем парсер с дальнейшим сохранением результатов в json
                system('clc||clear||CLS')
                self._parse_json()
            if result == MainMenuSett.FIELD_START_PARSER_RESULT_SAVE_CSV_MAIN_MENU:
                # Запускаем парсер с дальнейшим сохранением результатов в csv
                system('clc||clear||CLS')
                self._parse_csv()
            if result == MainMenuSett.FIELD_CLEAR_PARAMETERS_MAIN_MENU:
                # Вернуть все параметры в значения по умолчанию
                self._city = None
                self._marque = None
                self._model = None
                self._output_parameter = [True for _ in range(13)]
                self._d_get_par = dict()
                self._parser.clear_getparameters()
                self._parser.set_output_parameters(self._output_parameter)
            if result == MainMenuSett.FIELD_EXIT_MAIN_MENU:
                break  # Выходим из цикла и закрываем главное меню

    def _control_get_list_menu(self):
        """ Метод управления меню с установкой параметров через меню """
        while True:
            result = self._get_list_menu.start()
            if result == GetListMenuSett.FIELD_LIST_CITIES_GET_PARAMETERS_MENU:  # Выбор города
                city = self._cities_menu.start()
                self._city = city
            if result == GetListMenuSett.FIELD_LIST_MARQUES_GET_PARAMETERS_MENU:  # Выбор марки авто
                marque = self._marques_menu.start()
                self._marque = marque
                # После выбора марки, необходимо добавить поле с моделями и сгенерировать меню с моделями
                self._get_list_menu = Menu.GET_LIST_MENU
                self._create_menu_with_models(marque)
            if result == GetListMenuSett.FIELD_LIST_MODELS_GET_PARAMETERS_MENU:  # Выбор модели авто
                model = self._models_menu.start()
                self._model = model
            if result == GetListMenuSett.FIELD_LIST_OUTPUT_PARAMETERS_GET_PARAMETERS_MENU:  # Выбор выходных параметров
                l_output_parameters = self._outputs_par_menu.start()
                self._set_output_parameter_for_parser(l_output_parameters)
            if result == GetListMenuSett.FIELD_LIST_GET_PARAMETERS_GET_PARAMETERS_MENU:  # Выбор фильтров объявлений
                # Вызываем метод, который управляет меню фильтрации
                self._control_get_parameters_for_parser_menu()
            if result == GetListMenuSett.FIELD_RETURN_MAIN_MENU_GET_PARAMETERS_MENU:  # Возврат в главное меню
                # Возвращаем в главное меню
                break
            if result == GetListMenuSett.FIELD_EXIT_MAIN_MENU_GET_PARAMETERS_MENU:  # Выход
                # Выходим из CLI
                return MainMenuSett.FIELD_EXIT_MAIN_MENU

    def _set_output_parameter_for_parser(self, l_output_parameters_user):
        """ Метод установки выходных параметров

        :param l_output_parameters_user: Список, который содержит выбранные пользователем выходные данные
        """
        l_output_parameters = [False for _ in range(13)]
        # Из выбранных, пользователем, параметров заполняем список, который пойдет в парсер
        for parameter in l_output_parameters_user:
            if parameter == OutListMenuSett.FIELD_URL_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_URL_OUTPUT_PARAMETER] = True
            if parameter == OutListMenuSett.FIELD_PRICE_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_PRICE_OUTPUT_PARAMETER] = True
            if parameter == OutListMenuSett.FIELD_DESC_PRICE_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_DESC_PRICE_OUTPUT_PARAMETER] = True
            if parameter == OutListMenuSett.FIELD_CITY_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_CITY_PRICE_OUTPUT_PARAMETER] = True
            if parameter == OutListMenuSett.FIELD_DATE_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_DATE_OUTPUT_PARAMETER] = True
            if parameter == OutListMenuSett.FIELD_DESCRIPTION_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_DESCRIPTION_OUTPUT_PARAMETER] = True
            if parameter == OutListMenuSett.FIELD_PHOTO_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_PHOTO_OUTPUT_PARAMETERS] = True
            if parameter == OutListMenuSett.FIELD_ENGINE_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_ENGINE_OUTPUT_PARAMETERS] = True
            if parameter == OutListMenuSett.FIELD_POWER_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_POWER_OUTPUT_PARAMETERS] = True
            if parameter == OutListMenuSett.FIELD_TRANSMISSION_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_TRANSMISSION_OUTPUT_PARAMETERS] = True
            if parameter == OutListMenuSett.FIELD_COLOR_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_COLOR_OUTPUT_PARAMETERS] = True
            if parameter == OutListMenuSett.FIELD_MILEAGE_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_MILEAGE_OUTPUT_PARAMETER] = True
            if parameter == OutListMenuSett.FIELD_HAND_DRIVE_OUTPUT_PARAMETER_MENU:
                l_output_parameters[Parser.outputparameters.IND_HAND_DRIVE_OUTPUT_PARAMETER] = True
            if parameter == OutListMenuSett.FIELD_ALL_OUTPUT_PARAMETER_MENU:
                l_output_parameters = [True for _ in range(13)]
        # Устанавливаем выходные параметры для парсера
        self._output_parameter = l_output_parameters
        self._parser.set_output_parameters(l_output_parameters)

    def _control_get_parameters_for_parser_menu(self):
        """ Метод управления меню с фильтрацией объявлений """
        while True:
            result = self._get_par_menu.start()
            if result == GetParMenuSett.FIELD_DISTANCE_GETPARAMETERS_MENU:
                # Дополнительное расстояние поиска объявлений
                value = input_unsigned_int(GetParMenuSett.FIELD_DISTANCE_GETPARAMETERS_MENU)
                self._d_get_par[Parser.getparameters.DISTANCE_GET_GET_PARAMETER.get_name_str()] = value
            if result == GetParMenuSett.FIELD_MIN_PRICE_GETPARAMTERS_MENU:
                # Минимальная цена
                value = input_unsigned_int(GetParMenuSett.FIELD_MIN_PRICE_GETPARAMTERS_MENU)
                self._d_get_par[Parser.getparameters.MIN_PRICE_GET_PARAMETER] = value
            if result == GetParMenuSett.FIELD_MAX_PRICE_GETPARAMTERS_MENU:
                # Максимальная цена
                value = input_unsigned_int(GetParMenuSett.FIELD_MAX_PRICE_GETPARAMTERS_MENU)
                self._d_get_par[Parser.getparameters.MAX_PRICE_GET_PARAMETER] = value
            if result == GetParMenuSett.FIELD_MIN_YEAR_GETPARAMETERS_MENU:
                # Минимальный год выпуска автомобиля
                value = input_unsigned_int(GetParMenuSett.FIELD_MIN_YEAR_GETPARAMETERS_MENU)
                self._d_get_par[Parser.getparameters.MIN_YEAR_GET_PARAMETER] = value
            if result == GetParMenuSett.FIELD_MAX_YEAR_GETPARAMETERS_MENU:
                # Максимальный год выпуска автомобиля
                value = input_unsigned_int(GetParMenuSett.FIELD_MAX_YEAR_GETPARAMETERS_MENU)
                self._d_get_par[Parser.getparameters.MAX_YEAR_GET_PARAMETER] = value
            if result == GetParMenuSett.FIELD_TRANSMISSION_GETPARAMETERS_MENU:
                # Коробка передач (Меню)
                self._control_and_set_menu_with_more_parameters_for_getparameters(Menu.TRANSMISSION_MENU,
                                                                                  Parser.GET_Parameters.
                                                                                  TRANSMISSION_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_FUEL_GETPARAMETERS_MENU:
                # Топливо автомобиля (Меню)
                self._control_and_set_menu_with_one_parameter_for_getparameters(Menu.FUEL_MENU,
                                                                                Parser.GET_Parameters.
                                                                                FUEL_TYPE_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_MIN_ENGINE_CAPACITY_GETPARAMETERS_MENU:
                # Минимальный объем двигателя (Меню)
                self._control_and_set_menu_with_one_parameter_for_getparameters(Menu.MIN_ENGINE_CAPACITY_MENU,
                                                                                Parser.GET_Parameters.
                                                                                MIN_ENGINE_CAPACITY_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_MAX_ENGINE_CAPACITY_GETPARAMETERS_MENU:
                # Максимальный объем двигателя (Меню)
                self._control_and_set_menu_with_one_parameter_for_getparameters(Menu.MAX_ENGINE_CAPACITY_MENU,
                                                                                Parser.GET_Parameters.
                                                                                MAX_ENGINE_CAPACITY_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_WHEEL_DRIVE_GETPARAMETERS_MENU:
                # Привод автомобиля (меню)
                self._control_and_set_menu_with_one_parameter_for_getparameters(Menu.WHEEL_DRIVE_MENU,
                                                                                Parser.GET_Parameters.
                                                                                WHEEL_DRIVE_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_FRAME_GETPARAMETERS_MENU:
                # Кузов автомобиля (меню)
                self._control_and_set_menu_with_more_parameters_for_getparameters(Menu.FRAME_AUTO_MENU,
                                                                                  Parser.GET_Parameters.
                                                                                  FRAME_GET_AUTO_PARAMETER)
            if result == GetParMenuSett.FIELD_COLOR_GETPARAMETERS_MENU:
                # Цвет автомобиля (Меню)
                self._control_and_set_menu_with_one_parameter_for_getparameters(Menu.COLOR_AUTO_MENU,
                                                                                Parser.GET_Parameters.
                                                                                COLOR_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_DOCUMENT_GETPARAMETERS_MENU:
                # Состояние документов автомобиля (Меню)
                self._control_and_set_menu_with_one_parameter_for_getparameters(Menu.DOCUMENT_AUTO_MENU,
                                                                                Parser.GET_Parameters.
                                                                                DOCUMENT_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_DAMAGED_GETPARAMETERS_MENU:
                # Состояние автомобиля (Меню)
                self._control_and_set_menu_with_one_parameter_for_getparameters(Menu.DAMAGED_AUTO_MENU,
                                                                                Parser.GET_Parameters.
                                                                                DAMAGED_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_HAND_DRIVE_GETPARAMETERS_MENU:
                # Расположение руля в автомобиле (Меню)
                self._control_and_set_menu_with_one_parameter_for_getparameters(Menu.HAND_DRIVE_MENU,
                                                                                Parser.GET_Parameters.
                                                                                HAND_DRIVE_GET_PARAMETER)
            if result == GetParMenuSett.FIELD_MIN_POWER_GETPARAMETERS_MENU:
                # Минимальная мощность автомобиля
                value = input_unsigned_int(GetParMenuSett.FIELD_MIN_POWER_GETPARAMETERS_MENU)
                self._d_get_par[Parser.getparameters.MIN_POWER_GET_PARAMETER] = value
            if result == GetParMenuSett.FIELD_MAX_POWER_GETPARAMETERS_MENU:
                # Максимальная мощность автомобиля
                value = input_unsigned_int(GetParMenuSett.FIELD_MAX_POWER_GETPARAMETERS_MENU)
                self._d_get_par[Parser.getparameters.MAX_POWER_GET_PARAMETER] = value
            if result == GetParMenuSett.FIELD_MIN_MILEAGE_GETPARAMETERS_MENU:
                # Минимальный пробег автомобиля
                value = input_unsigned_int(GetParMenuSett.FIELD_MIN_MILEAGE_GETPARAMETERS_MENU)
                self._d_get_par[Parser.getparameters.MIN_MILEAGE_GET_PARAMETER] = value
            if result == GetParMenuSett.FIELD_MAX_MILEAGE_GETPARAMETERS_MENU:
                # Максимальный пробег автомобиля
                value = input_unsigned_int(GetParMenuSett.FIELD_MAX_MILEAGE_GETPARAMETERS_MENU)
                self._d_get_par[Parser.getparameters.MAX_MILEAGE_GET_PARAMETER] = value
            if result == GetParMenuSett.FIELD_OPEN_ADDIT_MENU_GETPARAMETER_MENU:
                # Установить дополнительный флаги фильтрации (меню)
                self._control_and_set_addit_menu_for_getparameters()
            if result == GetParMenuSett.FIELD_BACK_GETPARAMETERS_MENU:
                # Назад
                break
        # Устанавливаем GET-параметр в парсер
        if len(self._d_get_par) == 0:
            self._parser.clear_getparameters()
        else:
            for name, value in self._d_get_par.items():
                self._parser.set_getparameter(name, value)

    def _control_and_set_menu_with_more_parameters_for_getparameters(self, menu, get_parameter):
        """ Метод управления меню с несколькими выборами

        :param menu: Меню с выбором параметров
        :param get_parameter: Параметр, для которого происходит выбор
        """
        results = menu.start()
        try:
            dict_par = get_parameter.get_dict_parameters()
            values = []
            for result in results:
                values.append(dict_par[result])
            self._d_get_par[get_parameter.get_name_str()] = values
        except KeyError:  # Если пользователь выбрал назад, то ничего не делаем
            return None

    def _control_and_set_menu_with_one_parameter_for_getparameters(self, menu, get_parameter):
        """ Метод управления меню с одним выбором

        :param menu: Меню с выбором параметров
        :param get_parameter: Параметр, для которого происходит выбор
        """
        result = menu.start()
        try:
            dict_par = get_parameter.get_dict_parameters()
            value = dict_par[result]
            self._d_get_par[get_parameter.get_name_str()] = value
        except KeyError:  # Если пользователь выбрал назад, то ничего не делаем
            return None

    def _control_and_set_addit_menu_for_getparameters(self):
        """ Метод управления дополнительным меню с GET-параметрами и их установки """
        values = Menu.GET_PARAMETERS_ADDIT_MENU.start()
        for value in values:
            if value == GetParMenuSett.FIELD_UNSOLD_GETPARAMETERS_ADDIT_MENU:
                # Непроданные автомобили
                self._d_get_par[Parser.GET_Parameters.UNSOLD_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters.\
                    UNSOLD_GET_PARAMETER.unsold
            if value == GetParMenuSett.FIELD_ONLY_PHOTO_GETPARAMETERS_ADDIT_MENU:
                # Объявления только с фото
                self._d_get_par[Parser.GET_Parameters.PHOTO_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    PHOTO_GET_PARAMETER.photo
            if value == GetParMenuSett.FIELD_OWNER_SELLS_GETPARAMETERS_ADDIT_MENU:
                # Показывать только объявления от собственника
                self._d_get_par[Parser.GET_Parameters.OWNER_SELLS_GET_PARAMETER.get_name_str()] = Parser.\
                    GET_Parameters.OWNER_SELLS_GET_PARAMETER.owner
            if value == GetParMenuSett.FIELD_FOREIGN_GETPARAMETERS_ADDIT_MENU:
                # Только иностранные автомобили
                self._d_get_par[Parser.GET_Parameters.FOREIGN_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    FOREIGN_GET_PARAMETER.foreign
            if value == GetParMenuSett.FIELD_REPORT_GETPARAMETERS_ADDIT_MENU:
                # Показывать объявления только с отчетом от ГИБДД
                self._d_get_par[Parser.GET_Parameters.REPORT_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    REPORT_GET_PARAMETER.report
            if value == GetParMenuSett.FIELD_DROM_ASSIST_GETPARAMETERS_ADDIT_MENU:
                # Показывать объявления только прошедшие проверку от ДРОМ-ассистента
                self._d_get_par[Parser.GET_Parameters.DROM_GET_ASSIST_PARAMETER.get_name_str()] = Parser.\
                    GET_Parameters.DROM_GET_ASSIST_PARAMETER.assist
            if value == GetParMenuSett.FIELD_CERT_ASSIST_GETPARAMETERS_ADDIT_MENU:
                # Показывать объявления только сертифицированных автомобилей
                self._d_get_par[Parser.GET_Parameters.CERT_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    CERT_GET_PARAMETER.cert
            if value == GetParMenuSett.FIELD_TRADE_GETPARAMETERS_ADDIT_MENU:
                # Показывать объявления только в которых продавец не против обмена
                self._d_get_par[Parser.GET_Parameters.TRADE_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    TRADE_GET_PARAMETER.trade
            if value == GetParMenuSett.FIELD_ALL_GETPARAMETERS_ADDIT_MENU:
                # Выбрать все
                self._d_get_par[Parser.GET_Parameters.UNSOLD_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    UNSOLD_GET_PARAMETER.unsold
                self._d_get_par[Parser.GET_Parameters.PHOTO_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    PHOTO_GET_PARAMETER.photo
                self._d_get_par[Parser.GET_Parameters.OWNER_SELLS_GET_PARAMETER.get_name_str()] = Parser. \
                    GET_Parameters.OWNER_SELLS_GET_PARAMETER.owner
                self._d_get_par[Parser.GET_Parameters.FOREIGN_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    FOREIGN_GET_PARAMETER.foreign
                self._d_get_par[Parser.GET_Parameters.REPORT_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    REPORT_GET_PARAMETER.report
                self._d_get_par[Parser.GET_Parameters.DROM_GET_ASSIST_PARAMETER.get_name_str()] = Parser. \
                    GET_Parameters.DROM_GET_ASSIST_PARAMETER.assist
                self._d_get_par[Parser.GET_Parameters.CERT_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    CERT_GET_PARAMETER.cert
                self._d_get_par[Parser.GET_Parameters.TRADE_GET_PARAMETER.get_name_str()] = Parser.GET_Parameters. \
                    TRADE_GET_PARAMETER.trade
            if value == GetParMenuSett.FIELD_BACK_GETPARAMETERS_ADDIT_MENU:
                return None

    def _control_set_list_menu(self):
        """ Метод управления меню с установкой параметров """
        while True:
            result = self._set_list_menu.start()
            if result == SetListMenuSett.FIELD_LIST_CITIES_SET_PARAMETERS_MENU:
                input_mes = Mess.MESSAGE_INPUT_CITY
                # Задать город
                while True:
                    system('clc||clear||CLS')
                    city = input(input_mes)
                    # Если пользователь отменил ввод города
                    if city == Mess.MESSAGE_EXIT_INPUT:
                        break
                    # Получаем список доступных городов
                    l_cities = self._parser.get_available_cities()
                    if city in l_cities:  # Если веденный город есть в списке
                        self._city = city
                        break
                    else:  # Если веденного города нет в списках
                        input_mes = Mess.MESSAGE_INCORRECT_INPUT_CITY
            if result == SetListMenuSett.FIELD_LIST_MARQUES_SET_PARAMETERS_MENU:
                # Задать марку автомобиля
                input_mes = Mess.MESSAGE_INPUT_MARQUE
                while True:
                    system('clc||clear||CLS')
                    marque = input(input_mes)
                    # Если пользователь отменил ввод марки
                    if marque == Mess.MESSAGE_EXIT_INPUT:
                        break
                    # Получаем список доступных городов
                    l_marques = self._parser.get_available_marques()
                    if marque in l_marques:  # Если веденная марка есть в списке
                        self._marque = marque
                        break
                    else:  # Если веденной марки нет в списках
                        input_mes = Mess.MESSAGE_INCORRECT_INPUT_MARQUE
            if result == SetListMenuSett.FIELD_LIST_MODELS_SET_PARAMETERS_MENU:
                if self._marque is None:  # Если марка не задана, то необходимо сначала задать ее
                    # Задать марку автомобиля
                    input_mes = Mess.MESSAGE_INPUT_MARQUE
                    while True:
                        system('clc||clear||CLS')
                        marque = input(input_mes)
                        # Если пользователь отменил ввод марки
                        if marque == Mess.MESSAGE_EXIT_INPUT:
                            break
                        # Получаем список доступных городов
                        l_marques = self._parser.get_available_marques()
                        if marque in l_marques:  # Если веденная марка есть в списке
                            self._marque = marque
                            break
                        else:  # Если веденной марки нет в списках
                            input_mes = Mess.MESSAGE_INCORRECT_INPUT_MARQUE
                # Задать модель автомобиля
                input_mes = Mess.MESSAGE_INPUT_MODEL
                while True:
                    system('clc||clear||CLS')
                    model = input(input_mes)
                    # Если пользователь отменил ввод модели
                    if model == Mess.MESSAGE_EXIT_INPUT:
                        break
                    # Получаем список доступных городов
                    l_models = self._parser.get_available_models(self._marque)
                    if model in l_models:  # Если веденная модель есть в списке
                        self._model = model
                        break
                    else:  # Если веденной модели нет в списках
                        input_mes = Mess.MESSAGE_INCORRECT_INPUT_MODEL
            if result == SetListMenuSett.FIELD_RETURN_MAIN_MENU_SET_PARAMETERS_MENU:
                # Вернуться в главное меню
                break
            if result == SetListMenuSett.FIELD_EXIT_MAIN_MENU_SET_PARAMETERS_MENU:
                # Выйти
                return MainMenuSett.FIELD_EXIT_MAIN_MENU

    def _parse_json(self):
        """ Метод, который сохраняет полученные результаты от парсера в json файл  """
        d_result = self._parser.get_dict_with_parse_ads(city=self._city, marque=self._marque,
                                                        model=self._model, f_with_params=True)
        with open(f'{self._name_file}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(d_result, indent=4))

    def _parse_csv(self):
        """ Метод, который сохраняет полученные результаты от парсера в json файл """
        d_result = self._parser.get_dict_with_parse_ads(city=self._city, marque=self._marque,
                                                        model=self._model, f_with_params=True)
        csv_columns = [Parser.outputparameters.NAME_URL_OUTPUT_PARAMETER,
                       Parser.outputparameters.NAME_PRICE_OUTPUT_PARAMETER,
                       Parser.outputparameters.NAME_DESC_PRICE_OUTPUT_PARAMETER,
                       Parser.outputparameters.NAME_CITY_PRICE_OUTPUT_PARAMETER,
                       Parser.outputparameters.NAME_DATE_OUTPUT_PARAMETER,
                       Parser.outputparameters.NAME_DESCRIPTION_OUTPUT_PARAMETER,
                       Parser.outputparameters.NAME_PHOTO_OUTPUT_PARAMETERS,
                       Parser.outputparameters.NAME_ENGINE_OUTPUT_PARAMETERS,
                       Parser.outputparameters.NAME_POWER_OUTPUT_PARAMETERS,
                       Parser.outputparameters.NAME_TRANSMISSION_OUTPUT_PARAMETERS,
                       Parser.outputparameters.NAME_COLOR_OUTPUT_PARAMETERS,
                       Parser.outputparameters.NAME_MILEAGE_OUTPUT_PARAMETER,
                       Parser.outputparameters.NAME_HAND_DRIVE_OUTPUT_PARAMETER]
        with open(f'{self._name_file}.csv', 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()
            for num_page, data_page in d_result.items():
                for num_ads, data_ads in data_page.items():
                    for name_ad, data_ad in data_ads.items():
                        writer.writerow(data_ad)

    def __init__(self):
        # Выбранные параметры для парсера
        self._city = None
        self._marque = None
        self._model = None
        self._output_parameter = [True for _ in range(13)]
        self._d_get_par = dict()
        self._name_file = 'Drom_Parser'

        # Все меню
        self._main_menu = Menu.MAIN_MENU  # Главное меню
        self._get_list_menu = Menu.GET_LIST_MENU_DONT_MODELS  # Меню с установкой параметров через меню
        self._set_list_menu = Menu.SET_LIST_MENU  # Меню с установкой параметров
        self._cities_menu = Menu.Menu()  # Меню с выбором города
        self._marques_menu = Menu.Menu()  # Меню с выбором марки авто
        self._models_menu = Menu.Menu()  # Меню с выбором модели авто для соответствующей марки
        self._outputs_par_menu = Menu.OUTPUT_PARAMETERS_MENU  # Меню с выбором выходных параметров
        self._get_par_menu = Menu.GET_PARAMETERS_MENU  # Меня с фильтрами для объявлений
        # Сам парсер
        self._parser = Parser.DromParser()

        # Создаем меню с выбором города
        self._create_menu_with_cities()
        # Создаем меню с выбором марки авто
        self._create_menu_with_marques()

    def start(self):
        self._control_main_menu()
