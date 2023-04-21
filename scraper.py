import requests
from bs4 import BeautifulSoup

url = 'https://krew.info/zapasy/'

response = requests.get(url)
print(response.status_code)
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


def get_bank_status(row):
    bank_status = []
    imgs = row.find_all('img')
    # print(imgs)
    for img in imgs:
        bank_status.append(img.get('src'))
    # print(bank_status)
    return bank_status

blood_types = get_all_blood_types(rows)
cities = get_all_cities(rows)

bank_status = []

for row in rows:
    bank_status.append(get_bank_status(row))

blood_types_cities = {}
# bloodtype_i = 0
# city_i = 0

# print(cities)
# print(blood_types)

for count_cities, city in enumerate(cities):
    # if city_i > 20 or bloodtype_i > 7:
    #     break
    blood_types_cities[city] = {}
    for count_bd, blood_type in enumerate(blood_types):
        blood_types_cities[city][blood_type] = bank_status[count_bd][count_cities]
    #     bloodtype_i += 1
    # city_i += 1

import json
# print(blood_types_cities)
print(json.dumps(blood_types_cities, indent=2))

# TODO: main function for clarity


