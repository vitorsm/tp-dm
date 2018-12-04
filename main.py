import httplib2
import math
import json

url = "https://{}.olx.com.br/?o={}&q=fiat+uno"
h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

line_ident = '<li class="item" data-list_id="'
url_ident = 'href="'
page_amount_ident = '<span style="color: #999;font-weight: 400;">1 - '

car_motor_ident = '<span class="term">Potência do motor:</span>'
car_steering_ident = '<span class="term">Direção:</span>'
car_color_ident = '<span class="term">Cor:</span>'
car_only_owner_ident = '<span class="term">Único dono:</span>'
car_params_ident = 'self.adParams = '

begin_description_attribute_ident = '<strong class="description">'


states = ['mg', 'sp', 'rj', 'es', 'rs', 'sc', 'pr']
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
    print(page_text)
    index = page_text.find(car_params_ident)
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

    print("str data: " + data_str)
    data = json.loads(data_str)

    index = page_text.find(car_motor_ident)
    print("motor: " + str(index))
    if index >= 0:
        index += len(car_motor_ident)
        page_text = page_text[index:]
        index = page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        page_text = page_text[index:]
        index = page_text.find('<')
        data['motor'] = page_text[:index]
        data['motor'] = data['motor'].replace("\\n", '')
        data['motor'] = data['motor'].replace("\\t", '')
        data['motor'] = data['motor'].replace("\\", '')
        print(data['motor'])
        page_text = page_text[index:]

    index = page_text.find(car_steering_ident)
    print("steering: " + str(index))
    if index >= 0:
        index += len(car_steering_ident)
        page_text = page_text[index:]
        index = page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        page_text = page_text[:index]
        index = page_text.find('<')
        data['steering'] = page_text[:index]
        data['steering'] = data['steering'].replace("\\n", '')
        data['steering'] = data['steering'].replace("\\t", '')
        data['steering'] = data['steering'].replace("\\", '')
        print(data['steering'])
        page_text = page_text[index:]

    index = page_text.find(car_color_ident)
    print("color: " + str(index))
    if index >= 0:
        index += len(car_color_ident)
        page_text = page_text[index:]
        index = page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        page_text = page_text[:index]
        index = page_text.find('<')
        data['color'] = page_text[:index]
        data['color'] = data['color'].replace("\\n", '')
        data['color'] = data['color'].replace("\\t", '')
        data['color'] = data['color'].replace("\\", '')
        print(data['color'])
        page_text = page_text[index:]

    index = page_text.find(car_only_owner_ident)
    print("only_owner: " + str(index))
    if index >= 0:
        index += len(car_only_owner_ident)
        page_text = page_text[index:]
        index = page_text.find(begin_description_attribute_ident)
        index += len(begin_description_attribute_ident)
        page_text = page_text[:index]
        index = page_text.find('<')
        data['only_owner'] = page_text[:index]
        data['only_owner'] = data['only_owner'].replace("\\n", '')
        data['only_owner'] = data['only_owner'].replace("\\t", '')
        data['only_owner'] = data['only_owner'].replace("\\", '')
        print(data['only_owner'])
        page_text = page_text[index:]

    return data

### .......... Begin main method .......... ###


# json_str = "{\n\t\t\"brand\": \"FIAT\",\n\t\t\"model\": \"UNO\",\n\t\t\"version\": \"UNO MILLE 1.0 FIRE/ F.FLEX/ ECONOMY 4P\",\n\t\t\"year\": \"2009\",\n\t\t\"mileage\": \"165000\",\n\t\t\"fuel\": \"Flex\",\n\t\t\"gearbox\": \"Manual\",\n\t\t\"doors\": \"4 portas\",\n\t\t\"end_tag\": \"4\",\n\t\t\n\t\t\t\"extra\": \"alarme, trava el\xe9trica, vidro el\xe9trico, som\"\n\t\t\n\t}"
# json_dict = json.loads(json_str)
#
# print(json_dict)
# print(json_dict['version'])
# print(json_dict['fuel'])

for state in states:
    page_text = get_page(state, 1)
    pages_amount = get_max_page(page_text)

    page_text, car_url = get_car_url(page_text)

    page_text_car = get_car_page(car_url)

    data_car = get_car_data(page_text_car)
    print(data_car)
    break

