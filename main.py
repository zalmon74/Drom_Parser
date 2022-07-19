import Parser


# Объект с парсером
parser = Parser.DromParser()

# ИД
city = 'Красноярск'
marque = 'Honda'
model = 'Logo'
step_pages = 1

# Устанавливаем необходимый фильтр, через GET-параметр
parser.set_getparameter(Parser.getparameters.MIN_YEAR_GET_PARAMETER, 2015)
# Получаем спарсенные объявления
output = parser.get_dict_with_parse_ads(city=city, marque=marque, model=model, step_num_page=step_pages)
