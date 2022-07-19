import Parser
import time



parser = Parser.DromParser()

city = 'Красноярск'
marque = 'Honda'
model = 'Logo'
step_pages = 999999999999
output = parser.get_dict_with_parse_ads(city=city, marque=marque, model=model, step_num_page=step_pages)
for num_page, data_page in output.items():
    for num_ads, data_ads in data_page.items():
        for name_ad, data_ad in data_ads.items():
            pass


