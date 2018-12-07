import httplib2
import math
import json

url = "https://{}.olx.com.br/?o={}&q=fiat+uno"
h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

line_ident = '<li class="item" data-list_id="'
url_ident = 'href="'
page_amount_ident = '<span style="color: #999;font-weight: 400;">1 - '

car_motor_ident = '<span class="term">Pot\\xeancia do motor:</span>'
car_steering_ident = '<span class="term">Dire\\xe7\\xe3o:</span>'
car_color_ident = '<span class="term">Cor:</span>'
car_only_owner_ident = '<span class="term">\\xdanico dono:</span>'
car_type_ident = '<span class="term">Tipo de ve\\xedculo:</span>'
car_price_ident = 'template_vars.price = "'
car_params_ident = 'self.adParams = '

begin_description_attribute_ident = '<strong class="description">'

# states = ['mg', 'sp', 'rj', 'es']
states = ['sp', 'rj', 'es']

separator_csv_file = ';'

# page_text = "pagina web"

def get_car_url(page_text):
    index = page_text.find(line_ident)
    if index < 0:
        return None

    index += len(line_ident)
    page_text = page_text[index:]

    index = page_text.find(url_ident)
    if index < 0:
        return None

    index += len(url_ident)
    page_text = page_text[index:]

    index = page_text.find('"')
    if index < 0:
        return None

    end_url_index = index

    url_link = page_text[:end_url_index]
    url_link = url_link.replace('&amp;', '&')

    return page_text, url_link


def get_page(state, page_index):
    url_send = str.format(url, state, page_index)

    response, content = h.request(url_send)

    content = str(content)

    return content


def get_car_page(url):
    response, content = h.request(url)

    content = str(content)

    return content


def get_max_page(page_text):
    index = page_text.find(page_amount_ident)
    index += len(page_amount_ident)

    page_text = page_text[index:]

    amount_per_page_index = page_text.find(' de ')
    amount_per_page_str = page_text[:amount_per_page_index]

    amount_per_page_index += len(' de ')
    page_text = page_text[amount_per_page_index:]
    amount_items_index = page_text.find(' resultados')

    amount_items_str = page_text[:amount_items_index]

    amount_pages = float(amount_items_str) / float(amount_per_page_str)

    if amount_pages < 10:
        amount_pages *= 1000

    amount_pages_int = int(amount_pages)

    if amount_pages_int < amount_pages:
        amount_pages += 1

    return int(amount_pages)


def get_car_data(page_text):
    page_text = page_text.replace("\\n", "")
    page_text = page_text.replace("\\t", "")

    index = page_text.find(car_params_ident)

    if index < 0:
        return None, None


    index += len(car_params_ident)
    data_str = page_text[index:]

    index = data_str.find('}') + 1
    data_str = data_str[:index]
    data_str = data_str.replace("\\'", '"')
    data_str = data_str.replace("\\n", '')
    data_str = data_str.replace("\\t", '')
    data_str = data_str.replace("\\", '')
    data_str = data_str.strip()
    data_str = str(data_str)

    try:
        data = json.loads(data_str)
    except:
        return None, None

    if 'mileage' not in data or 'brand' not in data:
        return None, None

    index = page_text.find(car_motor_ident)
    data['motor'] = None
    if index >= 0:
        index += len(car_motor_ident)
        sub_page_text = page_text[index:]
        index = sub_page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        sub_page_text = sub_page_text[index:]
        index = sub_page_text.find('<')
        data['motor'] = sub_page_text[:index]
        data['motor'] = data['motor'].replace("\\n", '')
        data['motor'] = data['motor'].replace("\\t", '')
        data['motor'] = data['motor'].replace("\\", '')
        # page_text = page_text[index:]

    index = page_text.find(car_steering_ident)
    data['steering'] = None
    if index >= 0:
        index += len(car_steering_ident)
        sub_page_text = page_text[index:]
        index = sub_page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        sub_page_text = sub_page_text[index:]
        index = sub_page_text.find('<')
        data['steering'] = sub_page_text[:index]
        data['steering'] = data['steering'].replace("\\n", '')
        data['steering'] = data['steering'].replace("\\t", '')
        data['steering'] = data['steering'].replace("\\", '')
        # page_text = page_text[index:]

    index = page_text.find(car_color_ident)
    data['color'] = None
    if index >= 0:
        index += len(car_color_ident)
        sub_page_text = page_text[index:]
        index = sub_page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        sub_page_text = sub_page_text[index:]
        index = sub_page_text.find('<')
        data['color'] = sub_page_text[:index]
        data['color'] = data['color'].replace("\\n", '')
        data['color'] = data['color'].replace("\\t", '')
        data['color'] = data['color'].replace("\\", '')
        # page_text = page_text[index:]

    index = page_text.find(car_only_owner_ident)
    data['only_owner'] = None
    if index >= 0:
        index += len(car_only_owner_ident)
        sub_page_text = page_text[index:]
        index = sub_page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        sub_page_text = sub_page_text[index:]
        index = sub_page_text.find('<')
        data['only_owner'] = sub_page_text[:index]
        data['only_owner'] = data['only_owner'].replace("\\n", '')
        data['only_owner'] = data['only_owner'].replace("\\t", '')
        data['only_owner'] = data['only_owner'].replace("\\", '')
        # page_text = page_text[index:]

    index = page_text.find(car_type_ident)
    data['type'] = None
    if index >= 0:
        index += len(car_type_ident)
        sub_page_text = page_text[index:]
        index = sub_page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        sub_page_text = sub_page_text[index:]
        index = sub_page_text.find('<')
        data['type'] = sub_page_text[:index]
        data['type'] = data['type'].replace("\\n", '')
        data['type'] = data['type'].replace("\\t", '')
        data['type'] = data['type'].replace("\\", '')

    index = page_text.find(car_price_ident)
    data['price'] = None
    if index >= 0:
        index += len(car_price_ident)
        sub_page_text = page_text[index:]
        index = sub_page_text.find('"')
        data['price'] = sub_page_text[:index]

    extras = []
    if data['extra'] != '':
        extras = data['extra'].split(', ')


    return data, extras


### .......... Begin main method .......... ###


# json_str = "{\n\t\t\"brand\": \"FIAT\",\n\t\t\"model\": \"UNO\",\n\t\t\"version\": \"UNO MILLE 1.0 FIRE/ F.FLEX/ ECONOMY 4P\",\n\t\t\"year\": \"2009\",\n\t\t\"mileage\": \"165000\",\n\t\t\"fuel\": \"Flex\",\n\t\t\"gearbox\": \"Manual\",\n\t\t\"doors\": \"4 portas\",\n\t\t\"end_tag\": \"4\",\n\t\t\n\t\t\t\"extra\": \"alarme, trava el\xe9trica, vidro el\xe9trico, som\"\n\t\t\n\t}"
# json_dict = json.loads(json_str)
#
# print(json_dict)
# print(json_dict['version'])
# print(json_dict['fuel'])

def concatExtrasFile(extras):
    if extras == None:
        return

    extras_file = open('extras-file.csv', 'r+')
    text = extras_file.read()
    extrasSaved = None
    if text != None and text != '':
        extrasSaved = text.split(separator_csv_file)

    for extra in extras:
        if extrasSaved == None or extra not in extrasSaved:
            extras_file.write(extra + separator_csv_file)

def concatCarsFile(cars_file, car_data, state, car_url):
    cars_file.write('\r\n')

    void_str = ''

    if car_data['brand'] != None:
        cars_file.write(car_data['brand'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['model'] != None:
        cars_file.write(car_data['model'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    cars_file.write(state + separator_csv_file)

    if car_data['color'] != None:
        cars_file.write(car_data['color'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['mileage'] != None:
        cars_file.write(car_data['mileage'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['end_tag'] != None:
        cars_file.write(car_data['end_tag'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['fuel'] != None:
        cars_file.write(car_data['fuel'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['year'] != None:
        cars_file.write(car_data['year'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['gearbox'] != None:
        cars_file.write(car_data['gearbox'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['only_owner'] != None:
        cars_file.write(car_data['only_owner'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['type'] != None:
        cars_file.write(car_data['type'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['version'] != None:
        cars_file.write(car_data['version'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['steering'] != None:
        cars_file.write(car_data['steering'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['doors'] != None:
        cars_file.write(car_data['doors'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['extra'] != None:
        cars_file.write(car_data['extra'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    if car_data['price'] != None:
        cars_file.write(car_data['price'] + separator_csv_file)
    else:
        cars_file.write(void_str + separator_csv_file)

    cars_file.write(car_url + separator_csv_file)


extras_file = open('extras-file.csv', 'a')
cars_file = open('cars-file.csv', 'a')

extras_file = open('extras-file.csv', 'r+')
cars_file = open('cars-file.csv', 'r+')
dataset_file = open('dataset.csv', 'w+')

text = cars_file.read()

# if text == None or text == '':
#     cars_file.write('marca' + separator_csv_file)
#     cars_file.write('modelo' + separator_csv_file)
#     cars_file.write('estado' + separator_csv_file)
#     cars_file.write('cor' + separator_csv_file)
#     cars_file.write('quilometragem' + separator_csv_file)
#     cars_file.write('end_tag' + separator_csv_file)
#     cars_file.write('combustivel' + separator_csv_file)
#     cars_file.write('ano' + separator_csv_file)
#     cars_file.write('cambio' + separator_csv_file)
#     cars_file.write('unico_dono' + separator_csv_file)
#     cars_file.write('tipo' + separator_csv_file)
#     cars_file.write('versao' + separator_csv_file)
#     cars_file.write('direcao' + separator_csv_file)
#     cars_file.write('portas' + separator_csv_file)
#     cars_file.write('extra' + separator_csv_file)
#     cars_file.write('preco' + separator_csv_file)
#
#
# count = 0
# for i, state in enumerate(states):
#     page_text = get_page(state, 1)
#     pages_amount = get_max_page(page_text)
#
#     for page_index in range(1, pages_amount):
#         page_text = get_page(state, page_index)
#
#         for item_index in range(50):
#             page_text, car_url = get_car_url(page_text)
#             if page_text == None:
#                 break
#             else:
#                 print(car_url)
#                 page_text_car = get_car_page(car_url)
#
#                 if page_text_car != None:
#                     car_data, extras = get_car_data(page_text_car)
#                     if car_data != None and extras != None:
#                         concatExtrasFile(extras)
#                         concatCarsFile(cars_file, car_data, state, car_url)
#                         count += 1
#
#                 print("baixou " + str(count) + " itens")
#

extras_file = open('extras-file.csv', 'r')
cars_file = open('cars-file.csv', 'r')

extras = extras_file.read().split(separator_csv_file)


dataset_file.write('marca' + separator_csv_file)
dataset_file.write('modelo' + separator_csv_file)
dataset_file.write('estado' + separator_csv_file)
dataset_file.write('cor' + separator_csv_file)
dataset_file.write('quilometragem' + separator_csv_file)
dataset_file.write('end_tag' + separator_csv_file)
dataset_file.write('combustivel' + separator_csv_file)
dataset_file.write('ano' + separator_csv_file)
dataset_file.write('cambio' + separator_csv_file)
dataset_file.write('unico_dono' + separator_csv_file)
dataset_file.write('tipo' + separator_csv_file)
dataset_file.write('versao' + separator_csv_file)
dataset_file.write('direcao' + separator_csv_file)
dataset_file.write('portas' + separator_csv_file)
for extra in extras:
    if extra != '':
        dataset_file.write(extra + separator_csv_file)
dataset_file.write('preco' + separator_csv_file)

text_cars_file_line = cars_file.read().split('\n')
print(text_cars_file_line)

for i, line in enumerate(text_cars_file_line):
    print(i)
    if i > 0:
        dataset_file.write('\r\n')
        columns = line.split(separator_csv_file)

        if len(columns) >= 17:
            dataset_file.write(columns[0] + separator_csv_file)
            dataset_file.write(columns[1] + separator_csv_file)
            dataset_file.write(columns[2] + separator_csv_file)
            dataset_file.write(columns[3] + separator_csv_file)
            dataset_file.write(columns[4] + separator_csv_file)
            dataset_file.write(columns[5] + separator_csv_file)
            dataset_file.write(columns[6] + separator_csv_file)
            dataset_file.write(columns[7] + separator_csv_file)
            dataset_file.write(columns[8] + separator_csv_file)
            dataset_file.write(columns[9] + separator_csv_file)
            dataset_file.write(columns[10] + separator_csv_file)
            dataset_file.write(columns[11] + separator_csv_file)
            dataset_file.write(columns[12] + separator_csv_file)
            dataset_file.write(columns[13] + separator_csv_file)


            car_extras = columns[14].split(', ')
            for extra in extras:
                if extra != '':
                    if extra in car_extras:
                        dataset_file.write('1' + separator_csv_file)
                    else:
                        dataset_file.write('0' + separator_csv_file)

            dataset_file.write(columns[15] + separator_csv_file)
            dataset_file.write(columns[16] + separator_csv_file)