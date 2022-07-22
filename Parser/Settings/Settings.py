"""
Файл содержит настроечные параметры для парсера
"""


# Флаг печати на экран символов при парсинге страницы с объявлениями и одного объявления
F_PRINT_SYMBOLS = True

# Параметры для парсинга и определения доступных городов
ONLY_CITY_TAG_ALL_OBJ_PARAMETER_SETTING = 'noscript'  # Тэг содержит список всех городов на странице
ONLY_CITY_TAG_OBJ_PARAMETER_SETTING = 'a'  # Тэг содержит объект одного города
ONLY_CITY_LINK_PARAMETER_SETTING_SETTING = 'href'  # Значение, чтобы вытащить ссылку с объявления для данного города

# Параметры для парсинга и определения существующих марок
MARQUE_POPULAR_TAG_OBJ_PARAMETER_SETTING = 'div'  # Тэг для получения объекта с популярными марками авто на старинце
# Класс CSS для поиска объекта с пополярными марками авто
MARQUE_POPULAR_CLASS_CSS_OBJ_PARAMETER_SETTING = 'css-1q61nn e4ojbx42'
MARQUE_TAG_OBJ_PARAMETER_SETTING = 'a'  # Тэг для получения основных марок авто на странице
MARQUE_TAG_ALL_OBJ_PARAMETER_SETTING = 'noscript'  # Тэг для получения всех марок авто на странице
MARQUE_LINK_PARAMETER_SETTING = 'href'  # Значение, чтобы вытащить ссылку с объявления для данной марки
# Имя и значения поля, которому присваиваются различные параметры для их поиска на странице
MARQUE_NAME_OBJ_PARAMETER_SETTING = 'data-ftid'
MARQUE_DATA_OBJ_PARAMETER_SETTING = 'component_cars-list-item_hidden-link'
# Имя, которое необходимо заменить в URL, чтобы произвести фильтр объявлений по определенной марки авто
NAME_AUTO_URL_PARAMETER_SETTING = 'auto'

# Параметры для парсинга и определения доступных моделей авто для соответствующей марки
MODEL_TAG_ALL_OBJ_PARAMETER_SETTING = 'a'  # Тэг для получения всех объектов с доступными моделями
# CSS класс для получения всех объектов с доступными моделями
MODEL_CLASS_CSS_OBJ_PARAMETER_SETTING = 'e64vuai0 css-1i48p5q e104a11t0'
MODE_LINK_PARAMETER_SETTING = 'href'  # Значение, чтобы вытащить ссылку с объявления для данной модели

# Настроечные параметры для поиска объектов на странице с объявлением
# Название объявления
TITLE_TAG_OBJ_PARAMETER_SETTING = 'span'  # Тэг объекта с названием авто
# Имя и значение поля для поиска на странице объекта с названием объявления
TITLE_NAME_OBJ_PARAMETER_SETTING = 'data-ftid'
TITLE_DATA_OBJ_PARAMETER_SETTING = 'bull_title'

# Объявление на странице
ADS_TAG_OBJ_PARAMETER_SETTING = 'a'  # Тэг для поиска объекта с объявлением
# CSS класс для получения всех объектов с объявлением
ADS_CLASS_CSS_OBJ_PARAMETER_SETTING = 'css-1dlmvcl ewrty961'
ADS_LINK_PARAMETER_SETTING = 'href'  # Значение, чтобы вытащить ссылку с объявлением
# Имя и значение поля для поиска на странице объекта с названием объявления
ADS_NAME_OBJ_PARAMETER_SETTING = 'data-ftid'
ADS_DATA_OBJ_PARAMETER_SETTING = 'bulls-list_bull'

# Параметр "Описание авто"
FULL_DESCRIPTION_TAG_OBJ_PARAMETER_SETTING = 'div'  # Тэг для получения объекта с полным описанием объявления
# Класс CSS для поиска объекта с полным описанием объявления
FULL_DESCRIPTION_CLASS_CSS_OBJ_PARAMETER_SETTING = 'css-inmjwf e162wx9x0'
DESCRIPTION_TAG_OBJ_PARAMETER_SETTING = 'span'  # Тэг для получения объекта с описанием объявления
# Класс CSS для поиска объекта с описанием объявления
DESCRIPTION_CLASS_CSS_OBJ_PARAMETER_SETTING = 'css-1kb7l9z e162wx9x0'

# Параметр "Фото в объявлении"
PHOTO_TAG_ALL_OBJ_PARAMETER_SETTING = 'div'  # Тэг для поиска объекта в объявления, который содержит все фото
# Имя и значение поля для поиска на странице объекта с фото
PHOTO_NAME_OBJ_PARAMETER_SETTING = 'data-ftid'
PHOTO_DATA_OBJ_PARAMETER_SETTING = 'bull-page_bull-gallery_thumbnails'
PHOTO_TAG_OBJ_PARAMETER_SETTING = 'a'  # Тэг для поиска объекта в объявления, который содержит фото
PHOTO_LINK_PARAMETER_SETTING = 'href'  # значение, чтобы вытащить ссылку на фото

# Параметр "Описание двигателя"
ENGINE_TAG_OBJ_PARAMETER_SETTING = 'th'  # Тэг объекта с описанием двигателя авто
ENGINE_TEXT_PARAMETER_SETTING = 'Двигатель'  # Вспомогательный текст для поиска объекта с описанием двигателя

# Параметр "Мощность авто"
POWER_TAG_OBJ_PARAMETER_SETTING = 'th'  # Тэг объекта с описанием мощности авто
POWER_TEXT_PARAMETER_SETTING = 'Мощность'  # Вспомогательный текст для поиска объекта с мощностью авто

# Параметр "Коробка передач"
TRANSMISSION_TAG_OBJ_PARAMETER_SETTING = 'th'  # Тэг объекта с описанием коробки передач авто
TRANSMISSION_TEXT_PARAMETER_SETTING = 'Коробка передач'  # Вспомогательный текст для поиска объекта с коробкой передач

# Параметр "Цвет"
COLOR_TAG_OBJ_PARAMETER_SETTING = 'th'  # Тэг объекта с описанием цвета авто
COLOR_TEXT_PARAMETER_SETTING = 'Цвет'  # Вспомогательный текст для поиска объекта с цветом авто

# Параметр "Пробег авто"
MILEAGE_TAG_OBJ_PARAMETER_SETTING = 'th'  # Тэг объекта с описанием пробега авто
MILEAGE_TEXT_PARAMETER_SETTING = 'Пробег, км'   # Вспомогательный текст для поиска объекта с пробегом авто

# Параметр "Расположение руля"
HAND_DRIVE_TAG_OBJ_PARAMETER_SETTING = 'th'  # Тэг объекта с описанием расположения руля в авто
HAND_DRIVE_TEXT_PARAMETER_SETTING = 'Руль'  # Вспомогательный текст для поиска объекта с расположением руля в авто

# Параметр "Цена авто"
PRICE_TAG_OBJ_PARAMETER_SETTING = 'span'  # Тэг объекта с ценой авто
# Имя и значение поля для поиска на странице объекта с ценой авто
PRICE_NAME_OBJ_PARAMETER_SETTING = 'data-ftid'
PRICE_DATA_OBJ_PARAMETER_SETTING = 'bull_price'

# Параметр "Описание цены"
DESC_PRICE_TAG_OBJ_PARAMETER_SETTING = 'div'  # Тэг объекта с описанием цены авто
# Класс CSS для поиска объекта с описанием цены авто
DESC_PRICE_CLASS_CSS_OBJ_PARAMETER_SETTING = 'css-11m58oj evjskuu0'

# Параметр "Город"
CITY_TAG_OBJ_PARAMETER_SETTING = 'span'  # Тэг объекта, который описывает город
# Класс CSS для поиска объекта с описанием города
CITY_CLASS_CSS_OBJ_PARAMETER_SETTING = 'css-1488ad e162wx9x0'

# Параметр "Дата объявления"
DATE_TAG_OBJ_PARAMETER_SETTING = 'div'  # Тэг объекта с датой объявления
# Имя и значение поля для поиска на странице объекта с датой объявления
DATE_NAME_OBJ_PARAMETER_SETTING = 'data-ftid'
DATE_DATA_OBJ_PARAMETER_SETTING = 'bull_date'

