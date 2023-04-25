import requests, re
from bs4 import BeautifulSoup

url = 'https://krew.info/zapasy/'

response = requests.get(url)
# print(response.status_code)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')
# print(table)

"""
0 = stop
11 = full (but not halted)
1 = almost full
2 = half
3 = very low
"""

for blood_banks in table.find_all('tbody'):
    rows = blood_banks.find_all('tr')
    # print("rows:", rows)

# TODO: implement get_last_updated_timestamp
# def get_last_updated_timestamp(row):
#     pass


def fetch_all_cities_blood_types(row):
    pass


# ['0 Rh-', '0 Rh+', 'A Rh-', 'A Rh+', 'B Rh-', 'B Rh+', 'AB Rh-', 'AB Rh+']
def get_all_blood_types(rows):
    blood_types = []
    for row in rows:
        blood_types.append(row.find('h3').text)
    return blood_types

# ['Białystok', 'Bydgoszcz', 'Gdańsk', 'Kalisz', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Łódź', 'Olsztyn', 'Opole', 'Poznań', 'Racibórz', 'Radom', 'Rzeszów', 'Słupsk', 'Szczecin', 'Wałbrzych', 'Warszawa', 'Wrocław', 'Zielona Góra']
def get_all_cities(rows):
    cities = []
    for row in rows:
        imgs = row.find_all('img')
    for img in imgs:
        cities.append(img.get('alt'))
    return cities


def map_img_to_blood_type(img):
    match img:
        case "img/krew0.png":
            return "STOP"
        case "img/krew11.png":
            return "ALMOST_FULL"
        case "img/krew1.png":
            return "OPTIMAL"
        case "img/krew2.png":
            return "MODERATE"
        case "img/krew3.png":
            return "CRITICAL"


def get_bank_status(row):
    bank_status = []
    imgs = row.find_all('img')
    # print(imgs)
    for img in imgs:
        bank_status.append(map_img_to_blood_type(img.get('src')))
    # print(bank_status)
    return bank_status


def get_datetime_modified(soup):
    datetime_full = soup.find(string=re.compile("Aktualizacja stanu:")) # most reliable way for now, since this tag has no id
    return re.search(r'\d.+', datetime_full).group(0)

blood_types = get_all_blood_types(rows)
cities = get_all_cities(rows)

bank_status = []

for row in rows:
    bank_status.append(get_bank_status(row))

blood_banks = {}
output_json = {
    "datetime_modified": get_datetime_modified(soup),
    "url_src": response.url,
    "blood_banks": blood_banks
}

for count_cities, city in enumerate(cities):
    blood_banks[city] = {}
    for count_bd, blood_type in enumerate(blood_types):
        blood_banks[city][blood_type] = bank_status[count_bd][count_cities]

import json
print(json.dumps(output_json, indent=2, ensure_ascii=False))

# TODO: main function for clarity


