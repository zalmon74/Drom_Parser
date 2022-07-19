import unittest
import json
import http.server
import socketserver
from os import chdir
from threading import Thread

import requests

import Parser


class MySimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """ Создаем свой класс, чтобы не засорял поток вывода """

    def log_message(self, format_: str, *args) -> None:
        pass


class TestParserWithLocalServer(unittest.TestCase):
    """
    Тесты для проверки работоспособности класса DromParser
    """

    def _connection_test_server(self):
        """
        Метод проверяем подключение к локальному серверу
        """
        # Проверяем, что локальный сервер включен
        try:
            response = requests.get(self.home_url)
            self.assertTrue(response.ok)
        except requests.exceptions.ConnectionError:
            self.assertTrue(False, 'Локальный сервер выключен или недоступен')
        else:
            # Проверяем наличие нужных каталогов и файлов
            response = requests.get(f'{self.home_url + self.path_template_with_cities}')
            self.assertTrue(response.ok)
            response = requests.get(f'{self.home_url + self.path_template_with_marks}')
            self.assertTrue(response.ok)
            response = requests.get(f'{self.home_url + self.path_template_with_models}')
            self.assertTrue(response.ok)

    def setUp(self) -> None:
        self.ip = 'localhost'
        self.port = 8000
        self.home_url = f'http://{self.ip}:{self.port}/'
        self.path_template_with_cities = 'templates_for_tests/test_available_cities/city..html'
        self.path_template_with_marks = 'templates_for_tests/test_available_marques/mark.html'
        self.path_template_with_models = 'templates_for_tests/test_available_audi_models/model_audi.html'
        self.parser = Parser.DromParser(drom_url_cities=f'{self.home_url + self.path_template_with_cities}',
                                        drom_url_catalog=f'{self.home_url + self.path_template_with_marks}')
        self.mark_with_models = 'Audi'

        # Переходим на уровень выше
        chdir('..')

        # Запускаем сервер в другом потоке
        handler = MySimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer((self.ip, self.port), handler)
        self.server = Thread(target=self.httpd.serve_forever)
        self.server.start()

    def tearDown(self) -> None:
        # Выключаем сервер
        self.httpd.shutdown()
        self.httpd.server_close()
        # Возвращаемся обратно в нашу директорию
        chdir('UnitTests')

    def test_get_available_cities_with(self):
        """
        Метод проверки работоспособности метода 'get_available_cities'
        """
        # Проверяем работоспособность локального сервера
        self._connection_test_server()
        # Запускаем парсер на определение доступных городов
        available_cities = self.parser.get_available_cities()
        # Переконвертируем в кодировку cp1241
        available_cities_cp1251 = []
        for city in available_cities:
            city = city.encode('iso8859-1').decode('cp1251')
            available_cities_cp1251.append(city)
        # В 'data_for_test/available_cities.json' лежит список с правильными городами.
        # Считываем и сравниваем полученный список со считанным
        with open('data_for_test/available_cities.json', 'r') as file:
            correct_cities = json.load(file)
        self.assertListEqual(available_cities_cp1251, correct_cities,
                             'Парсер не верно считывает доступные города')

    def test_get_available_marques(self):
        """
        Тест проверяет работоспособность метода 'get_available_marques'
        :return:
        """
        # Проверяем работоспособность локального сервера
        self._connection_test_server()
        # Запускаем парсер на определение доступных марок авто
        available_marks = self.parser.get_available_marques()
        # Переконвертируем в кодировку cp1241
        available_marks_cp1251 = []
        for mark in available_marks:
            mark = mark.encode('iso8859-1').decode('cp1251')
            available_marks_cp1251.append(mark)
        # В 'data_for_test/available_marks.json' лежит список с правильными марками авто.
        # Считываем и сравниваем полученный список со считанным
        with open('data_for_test/available_marks.json', 'r') as file:
            correct_marks = json.load(file)
        self.assertListEqual(available_marks_cp1251, correct_marks,
                             'Парсер не верно считывает доступные марки авто')

    def test_get_available_models_for_audi(self):
        """
        Тест проверяет работоспособность метода
        """
        # Проверяем работоспособность локального сервера
        self._connection_test_server()
        # Запускаем парсер на определение доступных марок авто
        available_models = self.parser.get_available_models(self.mark_with_models)
        # В 'data_for_test/available_models_Audi.json' лежит список с правильными марками авто.
        # Считываем и сравниваем полученный список со считанным
        with open('data_for_test/available_models_Audi.json', 'r') as file:
            correct_models = json.load(file)
        self.assertListEqual(available_models, correct_models,
                             f'Парсер не верно считывает доступные модели')


class TestParser(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser.DromParser()
        self.get_par = Parser.getparameters.MIN_YEAR_GET_PARAMETER
        self.get_par_value = 2015

    def test_get_url_with_ads_error_incorrect_city(self):
        """ Тест на проверку получения ошибки некорректного города в методе 'get_url_with_ads' """
        # ИД
        incorrect_city = 'Красноярскк'
        correct_marque = 'Honda'
        incorrect_marque = 'Hoda'
        correct_model = 'Logo'
        incorrect_model = 'Lgo'
        # Только некорректный город
        url = self.parser.get_url_with_ads(city=incorrect_city)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        # Некорректный город с корректной маркой авто
        url = self.parser.get_url_with_ads(city=incorrect_city, marque=correct_marque)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        # Некорректный город с некорректной маркой авто
        url = self.parser.get_url_with_ads(city=incorrect_city, marque=incorrect_marque)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        # Некорректный город с корректной маркой и моделью авто
        url = self.parser.get_url_with_ads(city=incorrect_city, marque=correct_marque, model=correct_model)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        # Некорректный город с некорректной маркой и корректной моделью авто
        url = self.parser.get_url_with_ads(city=incorrect_city, marque=incorrect_marque, model=correct_model)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        # Некорректный город с некорректной маркой и моделью авто
        url = self.parser.get_url_with_ads(city=incorrect_city, marque=incorrect_marque, model=incorrect_model)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        # Некорректный город с корректной маркой и моделью авто, а также с дополнительными GET-параметрами
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        url = self.parser.get_url_with_ads(city=incorrect_city, marque=correct_marque, model=correct_model,
                                           f_with_params=True)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsInstance(self.parser.d_parameters, dict)
        self.assertNotEqual(len(self.parser.d_parameters), 0)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)

    def test_get_url_with_ads_error_incorrect_marque(self):
        """ Тест на проверку получения ошибки некорректной марки авто в методе 'get_url_with_ads' """
        # ИД
        correct_city = 'Красноярск'
        incorrect_marque = 'Hoda'
        correct_model = 'Logo'
        # Некорректная марка авто
        url = self.parser.get_url_with_ads(marque=incorrect_marque)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_MARQUE_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_marque)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        # Некорректная марка, но корректная модель авто
        url = self.parser.get_url_with_ads(marque=incorrect_marque, model=correct_model)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_MARQUE_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_marque)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        # Некорректная марка, но корректные модель авто и город
        url = self.parser.get_url_with_ads(marque=incorrect_marque, model=correct_model, city=correct_city)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_MARQUE_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_marque)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        # Некорректная марка, но корректные модель авто и город, а также включены дополнительные GET-параметры
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        url = self.parser.get_url_with_ads(marque=incorrect_marque, model=correct_model, city=correct_city,
                                           f_with_params=True)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_MARQUE_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_marque)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsInstance(self.parser.d_parameters, dict)
        self.assertNotEqual(len(self.parser.d_parameters), 0)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)

    def test_get_url_with_ads_error_model_without_marque(self):
        """
        Тест на проверку получения ошибки, которая получается при запросе модели без указания марки авто
        в методе 'get_url_with_ads'
        """
        # ИД
        correct_city = 'Красноярск'
        correct_model = 'Logo'
        # Задана модель без марки
        url = self.parser.get_url_with_ads(model=correct_model)
        self.assertEqual(url, Parser.Errors.ERROR_MODEL_WITHOUT_MARQUE)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNone(self.parser.d_marque_href)
        self.assertIsNone(self.parser.d_model_href)
        # Задана модель без марки, но с городом
        url = self.parser.get_url_with_ads(model=correct_model, city=correct_city)
        self.assertEqual(url, Parser.Errors.ERROR_MODEL_WITHOUT_MARQUE)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNone(self.parser.d_marque_href)
        self.assertIsNone(self.parser.d_model_href)
        # Задана модель без марки, но с городом и с дополнительными GET-параметрами
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        url = self.parser.get_url_with_ads(model=correct_model, city=correct_city, f_with_params=True)
        self.assertEqual(url, Parser.Errors.ERROR_MODEL_WITHOUT_MARQUE)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNone(self.parser.d_marque_href)
        self.assertIsNone(self.parser.d_model_href)
        self.assertIsNone(self.parser.d_city_href)
        self.assertNotEqual(len(self.parser.d_parameters), 0)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)

    def test_get_url_with_ads_error_incorrect_model(self):
        """ Тест на проверку получения ошибки некорректной модели авто в методе 'get_url_with_ads' """
        # ИД
        correct_city = 'Красноярск'
        correct_marque = 'Honda'
        incorrect_model = 'Lgo'
        # Некорректная модель с корректной маркой
        url = self.parser.get_url_with_ads(marque=correct_marque, model=incorrect_model)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_MODEL_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertIsInstance(self.parser.d_model_href, dict)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        # Некорректная модель с корректной маркой и городом
        url = self.parser.get_url_with_ads(marque=correct_marque, model=incorrect_model, city=correct_city)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_MODEL_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertIsInstance(self.parser.d_model_href, dict)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        # Некорректная модель с корректной маркой и городом и дополнительными GET-параметрами
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        url = self.parser.get_url_with_ads(marque=correct_marque, model=incorrect_model, city=correct_city,
                                           f_with_params=True)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_MODEL_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertIsInstance(self.parser.d_model_href, dict)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_parameters, dict)
        self.assertNotEqual(len(self.parser.d_parameters), 0)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)

    def test_get_url_with_ads(self):
        """ Тест метода 'get_url_with_ads' с корректными данными """
        # ИД
        city = 'Красноярск'
        marque = 'Honda'
        model = 'Logo'
        # Получаем URL с объявлениями в одном городе
        url = self.parser.get_url_with_ads(city=city)
        self.assertIsInstance(url, str)
        self.assertEqual(self.parser.current_url, url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertEqual(self.parser.d_city_href[city], url)
        response = requests.get(url)
        self.assertTrue(response.ok, f'Запрос на полученную URL имеет код {response.status_code}')
        # Получаем URL с объявлениями для соответствующей марки
        url = self.parser.get_url_with_ads(marque=marque)
        self.assertIsInstance(url, str)
        self.assertEqual(self.parser.current_url, url)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertEqual(self.parser.current_marque, marque)
        response = requests.get(url)
        self.assertTrue(response.ok, f'Запрос на полученную URL имеет код {response.status_code}')
        # Получаем URL с объявлениями для соответствующей марки и модели авто
        url = self.parser.get_url_with_ads(marque=marque, model=model)
        self.assertIsInstance(url, str)
        self.assertEqual(self.parser.current_url, url)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertEqual(self.parser.current_marque, marque)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        self.assertEqual(self.parser.current_model, model)
        response = requests.get(url)
        self.assertTrue(response.ok, f'Запрос на полученную URL имеет код {response.status_code}')
        # Получаем URL с объявлениями для определенного города и соответствующей марки авто
        url = self.parser.get_url_with_ads(city=city, marque=marque)
        self.assertIsInstance(url, str)
        self.assertEqual(self.parser.current_url, url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertEqual(self.parser.current_marque, marque)
        response = requests.get(url)
        self.assertTrue(response.ok, f'Запрос на полученную URL имеет код {response.status_code}')
        # Получаем URL с объявлениями для определенного города и соответствующей марки и модели авто
        url = self.parser.get_url_with_ads(city=city, marque=marque, model=model)
        self.assertIsInstance(url, str)
        self.assertEqual(self.parser.current_url, url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertEqual(self.parser.current_marque, marque)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        self.assertEqual(self.parser.current_model, model)
        response = requests.get(url)
        self.assertTrue(response.ok, f'Запрос на полученную URL имеет код {response.status_code}')
        # Получаем URL с объявлениями для определенного города и соответствующей марки и модели авто
        # И дополнительными GET-параметрами
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        url = self.parser.get_url_with_ads(city=city, marque=marque, model=model, f_with_params=True)
        self.assertIsInstance(url, str)
        self.assertEqual(self.parser.current_url, url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertEqual(self.parser.current_marque, marque)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        self.assertEqual(self.parser.current_model, model)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)
        response = requests.get(url)
        self.assertTrue(response.ok, f'Запрос на полученную URL имеет код {response.status_code}')

    def test_get_dict_with_parse_ads_with_error_incorrect_city(self):
        """ Тест на получение ошибки некорректного города для метода 'get_dict_with_parse_ads' """
        # ИД
        incorrect_city = 'Красноярскк'
        correct_marque = 'Honda'
        incorrect_marque = 'Hoda'
        correct_model = 'Logo'
        incorrect_model = 'Lgo'
        # Только некорректный город
        out_dic = self.parser.get_dict_with_parse_ads(city=incorrect_city)
        self.assertEqual(out_dic, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректный город с корректной маркой авто
        out_dic = self.parser.get_dict_with_parse_ads(city=incorrect_city, marque=correct_marque)
        self.assertEqual(out_dic, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректный город с некорректной маркой авто
        out_dic = self.parser.get_dict_with_parse_ads(city=incorrect_city, marque=incorrect_marque)
        self.assertEqual(out_dic, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректный город с корректной маркой и моделью авто
        out_dic = self.parser.get_dict_with_parse_ads(city=incorrect_city, marque=correct_marque, model=correct_model)
        self.assertEqual(out_dic, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректный город с некорректной маркой и корректной моделью авто
        out_dic = self.parser.get_dict_with_parse_ads(city=incorrect_city, marque=incorrect_marque, model=correct_model)
        self.assertEqual(out_dic, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректный город с некорректной маркой и моделью авто
        url = self.parser.get_dict_with_parse_ads(city=incorrect_city, marque=incorrect_marque, model=incorrect_model)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректный город с корректной маркой и моделью авто, а также с дополнительными GET-параметрами
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        out_dic = self.parser.get_dict_with_parse_ads(city=incorrect_city, marque=correct_marque, model=correct_model,
                                                      f_with_params=True)
        self.assertEqual(out_dic, Parser.Errors.ERROR_INCORRECT_CITY)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsInstance(self.parser.d_parameters, dict)
        self.assertNotEqual(len(self.parser.d_parameters), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)

    def test_get_dict_with_parse_ads_with_error_incorrect_marque(self):
        """ Тест на получение ошибки некорректной марки для метода 'get_dict_with_parse_ads' """
        # ИД
        correct_city = 'Красноярск'
        incorrect_marque = 'Hoda'
        correct_model = 'Logo'
        # Некорректная марка авто
        out_dict = self.parser.get_dict_with_parse_ads(marque=incorrect_marque)
        self.assertEqual(out_dict, Parser.Errors.ERROR_INCORRECT_MARQUE_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_marque)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректная марка, но корректная модель авто
        out_dict = self.parser.get_dict_with_parse_ads(marque=incorrect_marque, model=correct_model)
        self.assertEqual(out_dict, Parser.Errors.ERROR_INCORRECT_MARQUE_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_marque)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректная марка, но корректные модель авто и город
        url = self.parser.get_dict_with_parse_ads(marque=incorrect_marque, model=correct_model, city=correct_city)
        self.assertEqual(url, Parser.Errors.ERROR_INCORRECT_MARQUE_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_marque)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректная марка, но корректные модель авто и город, а также включены дополнительные GET-параметры
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        out_dict = self.parser.get_dict_with_parse_ads(marque=incorrect_marque, model=correct_model, city=correct_city,
                                                       f_with_params=True)
        self.assertEqual(out_dict, Parser.Errors.ERROR_INCORRECT_MARQUE_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_marque)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsInstance(self.parser.d_parameters, dict)
        self.assertNotEqual(len(self.parser.d_parameters), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)

    def test_get_dict_with_parse_ads_with_error_without_marque(self):
        """
        Тест на получение ошибки, которая получается при запросе модели без указания марки авто,
        в методе 'get_dict_with_parse_ads'
        """
        # ИД
        correct_city = 'Красноярск'
        correct_model = 'Logo'
        # Задана модель без марки
        out_dict = self.parser.get_dict_with_parse_ads(model=correct_model)
        self.assertEqual(out_dict, Parser.Errors.ERROR_MODEL_WITHOUT_MARQUE)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNone(self.parser.d_marque_href)
        self.assertIsNone(self.parser.d_model_href)
        self.assertIsNone(self.parser.d_parse_ads)
        # Задана модель без марки, но с городом
        out_dict = self.parser.get_dict_with_parse_ads(model=correct_model, city=correct_city)
        self.assertEqual(out_dict, Parser.Errors.ERROR_MODEL_WITHOUT_MARQUE)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNone(self.parser.d_marque_href)
        self.assertIsNone(self.parser.d_model_href)
        self.assertIsNone(self.parser.d_parse_ads)
        # Задана модель без марки, но с городом и с дополнительными GET-параметрами
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        out_dict = self.parser.get_dict_with_parse_ads(model=correct_model, city=correct_city, f_with_params=True)
        self.assertEqual(out_dict, Parser.Errors.ERROR_MODEL_WITHOUT_MARQUE)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNone(self.parser.d_marque_href)
        self.assertIsNone(self.parser.d_model_href)
        self.assertIsNone(self.parser.d_city_href)
        self.assertNotEqual(len(self.parser.d_parameters), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)

    def test_get_dict_with_parse_ads_with_error_incorrect_model(self):
        """ Тест на получение ошибки некорректной модели для метода 'get_dict_with_parse_ads' """
        # ИД
        correct_city = 'Красноярск'
        correct_marque = 'Honda'
        incorrect_model = 'Lgo'
        # Некорректная модель с корректной маркой
        out_dict = self.parser.get_dict_with_parse_ads(marque=correct_marque, model=incorrect_model)
        self.assertEqual(out_dict, Parser.Errors.ERROR_INCORRECT_MODEL_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertIsInstance(self.parser.d_model_href, dict)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректная модель с корректной маркой и городом
        out_dict = self.parser.get_dict_with_parse_ads(marque=correct_marque, model=incorrect_model, city=correct_city)
        self.assertEqual(out_dict, Parser.Errors.ERROR_INCORRECT_MODEL_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertIsInstance(self.parser.d_model_href, dict)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_city_href, dict)
        self.assertNotEqual(len(self.parser.d_city_href), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        # Некорректная модель с корректной маркой и городом и дополнительными GET-параметрами
        output = self.parser.set_getparameter(parameter=self.get_par, value=self.get_par_value)
        self.assertIsNone(output)
        out_dict = self.parser.get_dict_with_parse_ads(marque=correct_marque, model=incorrect_model, city=correct_city,
                                                       f_with_params=True)
        self.assertEqual(out_dict, Parser.Errors.ERROR_INCORRECT_MODEL_AUTO)
        self.assertIsNone(self.parser.current_url)
        self.assertIsNone(self.parser.current_model)
        self.assertIsNotNone(self.parser.d_marque_href)
        self.assertIsInstance(self.parser.d_marque_href, dict)
        self.assertNotEqual(len(self.parser.d_marque_href), 0)
        self.assertIsNotNone(self.parser.d_model_href)
        self.assertIsInstance(self.parser.d_model_href, dict)
        self.assertNotEqual(len(self.parser.d_model_href), 0)
        self.assertIsNotNone(self.parser.d_city_href)
        self.assertIsInstance(self.parser.d_parameters, dict)
        self.assertNotEqual(len(self.parser.d_parameters), 0)
        self.assertIsNone(self.parser.d_parse_ads)
        self.assertEqual(self.parser.d_parameters[self.get_par.get_name_str()], self.get_par_value)

    def test_get_dict_with_parse_ads(self):
        """ Тест с корректными аргументами для метода 'get_dict_with_parse_ads' """
        # ИД
        city = 'Красноярск'
        marque = 'Honda'
        model = 'Logo'
        step_pages = 999999999999  # Чтобы для обработки была всего одна страница - не затягивать юнит-тесты
        # Получаем спарсенные объявления в словаре
        out_dict = self.parser.get_dict_with_parse_ads(city=city, marque=marque, model=model, step_num_page=step_pages)
        self.assertIsInstance(out_dict, dict)
        self.assertDictEqual(out_dict, self.parser.d_parse_ads)
        for num_page, data_page in out_dict.items():
            self.assertIsInstance(num_page, int)
            self.assertIsInstance(data_page, dict)
            for num_ads, data_ads in data_page.items():
                self.assertIsInstance(num_ads, int)
                self.assertIsInstance(data_ads, dict)
                for name_ad, data_ad in data_ads.items():
                    self.assertIsInstance(name_ad, str)
                    self.assertEqual(len(data_ad), 13)
                    # Проверяем наличие всех спарсенных данных
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_URL_OUTPUT_PARAMETER], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_URL_OUTPUT_PARAMETER], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_PHOTO_OUTPUT_PARAMETERS], (list, str))
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_PHOTO_OUTPUT_PARAMETERS], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_CITY_PRICE_OUTPUT_PARAMETER], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_CITY_PRICE_OUTPUT_PARAMETER], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_COLOR_OUTPUT_PARAMETERS], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_COLOR_OUTPUT_PARAMETERS], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_PRICE_OUTPUT_PARAMETER], (int, str))
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_PRICE_OUTPUT_PARAMETER], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_HAND_DRIVE_OUTPUT_PARAMETER], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_HAND_DRIVE_OUTPUT_PARAMETER], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_DESC_PRICE_OUTPUT_PARAMETER], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_DESC_PRICE_OUTPUT_PARAMETER], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_DATE_OUTPUT_PARAMETER], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_DATE_OUTPUT_PARAMETER], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_DESCRIPTION_OUTPUT_PARAMETER], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_DESCRIPTION_OUTPUT_PARAMETER], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_ENGINE_OUTPUT_PARAMETERS], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_ENGINE_OUTPUT_PARAMETERS], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_MILEAGE_OUTPUT_PARAMETER], (int, str))
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_MILEAGE_OUTPUT_PARAMETER], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_POWER_OUTPUT_PARAMETERS], (int, str))
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_POWER_OUTPUT_PARAMETERS], 0)
                    self.assertIsInstance(data_ad[Parser.outputparameters.NAME_TRANSMISSION_OUTPUT_PARAMETERS], str)
                    self.assertNotEqual(data_ad[Parser.outputparameters.NAME_TRANSMISSION_OUTPUT_PARAMETERS], 0)

    def test_set_getparameter_with_errors(self):
        """ Тест на получение соответствующих ошибок для метода 'set_getparameter' """
        # ИД
        get_par_one_value = Parser.getparameters.MIN_YEAR_GET_PARAMETER
        get_par_more_values = Parser.getparameters.FRAME_GET_AUTO_PARAMETER
        value = 2015
        values = [1, 3, 4]
        incorrect_value = 2
        # Получение ошибки "ERROR_INCORRECT_GET_PARAMETER"
        self.assertEqual(len(self.parser.d_parameters), 0)
        error = self.parser.set_getparameter(parameter=Parser.getparameters.ParameterMinYear, value=value)
        self.assertEqual(error, Parser.Errors.ERROR_INCORRECT_GET_PARAMETER)
        self.assertEqual(len(self.parser.d_parameters), 0)
        # Получение ошибки "ERROR_INCORRECT_COUNT_ARG_FOR_GET_PARAMETER" - параметр может иметь только один аргумент
        self.assertEqual(len(self.parser.d_parameters), 0)
        error = self.parser.set_getparameter(parameter=get_par_one_value, value=values)
        self.assertEqual(error, Parser.Errors.ERROR_INCORRECT_COUNT_ARG_FOR_GET_PARAMETER)
        self.assertEqual(len(self.parser.d_parameters), 0)
        # Получение ошибки "ERROR_INCORRECT_ARGUMENT_FOR_GET_PARAMETER" - параметр не может иметь данный аргумент
        self.assertEqual(len(self.parser.d_parameters), 0)
        error = self.parser.set_getparameter(parameter=get_par_more_values, value=incorrect_value)
        self.assertEqual(error, Parser.Errors.ERROR_INCORRECT_ARGUMENT_FOR_GET_PARAMETER)
        self.assertEqual(len(self.parser.d_parameters), 0)

    def test_set_getparameter(self):
        """ Тест для проверки работоспособности метода 'set_getparameter' """
        # ИД
        get_par_one_value = Parser.getparameters.MIN_YEAR_GET_PARAMETER
        get_par_more_values = Parser.getparameters.FRAME_GET_AUTO_PARAMETER
        value = 2015
        values = [1, 3, 4]
        # Устанавливаем параметры и проверяем соответствие установленных парамтеров
        # Первый параметр с одним аргументом
        self.assertEqual(len(self.parser.d_parameters), 0)
        error = self.parser.set_getparameter(get_par_one_value, value=value)
        self.assertIsNone(error)
        self.assertEqual(len(self.parser.d_parameters), 1)
        self.assertEqual(self.parser.d_parameters[get_par_one_value.get_name_str()], value)
        # Второй параметр с несколькими аргументами
        error = self.parser.set_getparameter(get_par_more_values, value=values)
        self.assertIsNone(error)
        self.assertEqual(len(self.parser.d_parameters), 2)
        self.assertListEqual(self.parser.d_parameters[get_par_more_values.get_name_str()], values)

    def test_set_output_parameters(self):
        """
        Тест для проверки работоспособности метода установки выходных параметров 'set_output_parameters'
        Проверять каждый выходной параметр проверять смысла нет - это займет много времени. Парсинг
        небольшой деревни занимает примерно 30 секунд. Если каждый параметр проверять, то займет около 7 минут, что
        для юнит-тестов не приемлемо. Проверим только один параметр.

        P.S. Для тестов будет использована деревня с маленьким количеством объявлений
        Всегда будут объявления в каких нибудь ближайших городах, поэтому пустых словарей не будет
        """
        # ИД
        city = 'Большая Ирба'
        # Проверка - исключим из выходных параметров URL на объявление и фото
        self.parser.set_output_parameters(f_url=False, f_photo=False)
        # Парсим объявления и получаем словарь
        output_dict = self.parser.get_dict_with_parse_ads(city=city)
        self.assertIsInstance(output_dict, dict)
        # Проверяем, что исключенные параметры отсутствуют
        for page, d_data_page in output_dict.items():
            for num_ads, d_data in d_data_page.items():
                self.assertNotEqual(len(d_data), 0)
                try:
                    test_value = d_data[Parser.outputparameters.NAME_URL_OUTPUT_PARAMETER]
                except KeyError:  # Если данный параметр отсутствует, значит тест прошел
                    self.assertTrue(True)
                else:  # Если данный параметр присутствует, значит тест не прошел
                    self.assertTrue(False)
                try:
                    test_value = d_data[Parser.outputparameters.NAME_PHOTO_OUTPUT_PARAMETERS]
                except KeyError:  # Если данный параметр отсутствует, значит тест прошел
                    self.assertTrue(True)
                else:  # Если данный параметр присутствует, значит тест не прошел
                    self.assertTrue(False)

    def test_clear_getparameters(self):
        """ Тест для проверки работоспособности метода очистки словаря с GET-параметрами """
        # ИД
        get_par_one_value = Parser.getparameters.MIN_YEAR_GET_PARAMETER
        get_par_more_values = Parser.getparameters.FRAME_GET_AUTO_PARAMETER
        value = 2015
        values = [1, 3, 4]
        # Проверка очистки
        error = self.parser.set_getparameter(get_par_one_value, value=value)
        self.assertIsNone(error)
        error = self.parser.set_getparameter(get_par_more_values, value=values)
        self.assertIsNone(error)
        self.assertEqual(len(self.parser.d_parameters), 2)
        self.parser.clear_getparameters()
        self.assertEqual(len(self.parser.d_parameters), 0)
