from os import system

import CLI_Settings.Messages as Settings


class Menu:
    """ Описывает любое созданное меню, на экране консоли """

    def _print_menu(self):
        """ Метод вывода на экран всех полей меню """

        num = 1
        for string in self._l_menu:
            print(f'{num}. {string}')
            num += 1

    def __init__(self, f_more_parameters: bool = False):
        """
        :param f_more_parameters: Флаг, определяющий возможность выбора нескольких параметров из меню
        """
        self._l_menu = []  # Элемент = одна запись в меню
        self._next_num = 1  # Содержит следующее значение в меню
        self._f_more_parameters = f_more_parameters

        self._message_input = Settings.MESSAGE_INPUT_MENU

        self.f_clear = True  # Флаг отчистки экрана при не правильном выборе пользователем

    def add_field(self, string: str):
        """ Метод добавления нового пункта в меню """
        self._l_menu.append(string)
        self._next_num += 1

    def start(self) -> str:
        """
        Метод запуска работы меню

        :return: Возвращает выбранную строку из меню
        """

        while True:
            # Очищаем консоль перед выводом меню
            if self.f_clear:
                system('clc||clear||CLS')
            # Выводим меню на экран
            self._print_menu()
            # Запрашиваем от пользователя значение из меню
            print('\n')
            input_user = input(self._message_input)
            # Переводим введенное значение в int
            try:
                if self._f_more_parameters:
                    input_user = input_user.split()
                    input_user = [int(el) for el in input_user]
                else:
                    input_user = int(input_user)
            except ValueError:
                self._message_input = Settings.MESSAGE_INCORRECT_INPUT_MENU
            else:
                if self._f_more_parameters:
                    output = []
                    f_stop_inf = True
                    for el in input_user:
                        # Проверяем, что значение из меню выбрано правильно
                        if el < self._next_num:
                            output.append(self._l_menu[el - 1])
                        else:
                            self._message_input = Settings.MESSAGE_INCORRECT_INPUT_MENU
                            f_stop_inf = False
                            break  # Запрашиваем у пользователя новые данные
                    if f_stop_inf:  # Если все значения были выбраны правильно
                        break
                else:
                    # Проверяем, что значение из меню выбрано правильно
                    if input_user < self._next_num:
                        output = self._l_menu[input_user-1]
                        break
                    else:
                        self._message_input = Settings.MESSAGE_INCORRECT_INPUT_MENU
        return output

    def clear_menu(self):
        """ Метод очистки меню """
        self._l_menu.clear()
