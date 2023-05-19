import requests, re, json, os
import dateutil.parser
from bs4 import BeautifulSoup

source_url = 'https://krew.info/zapasy/'

try:
    api_url = os.environ['API_URL']
    api_token = os.environ['API_TOKEN']
except KeyError as e:
    raise KeyError("Please set the environment variable {}".format(e))

# ['0 Rh-', '0 Rh+', 'A Rh-', 'A Rh+', 'B Rh-', 'B Rh+', 'AB Rh-', 'AB Rh+']
def get_all_blood_types(rows):
    blood_types = []
    for row in rows:
        blood_types.append(row.find('strong').text)
    return blood_types


# ['Białystok', 'Bydgoszcz', 'Gdańsk', 'Kalisz', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Łódź', 'Olsztyn', 'Opole', 'Poznań', 'Racibórz', 'Radom', 'Rzeszów', 'Słupsk', 'Szczecin', 'Wałbrzych', 'Warszawa', 'Wrocław', 'Zielona Góra']
def get_all_cities(rows):
    cities = []
    imgs = []
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
    for img in imgs:
        bank_status.append(map_img_to_blood_type(img.get('src')))
    return bank_status


def get_datetime_modified(soup):
    datetime_full = re.search(r'\d.+', soup.find(string=re.compile("Aktualizacja stanu:"))).group(0) # most reliable way for now, since this tag has no id
    datetime_iso8601 = (dateutil.parser.parse(datetime_full)).isoformat() + "+02:00"
    return datetime_iso8601


def post_to_api(json, api_token):
    auth_header = {'Authorization': 'Token ' + api_token}
    response = requests.post(api_url, json=json,headers=auth_header)
    print("Response status code:", response.status_code)
    if response.text:
        print("Response text:", response.text)


def main():
    bank_status = []
    blood_banks = {}
    rows = []
    
    source_response = requests.get(source_url)
    source_response.encoding = 'utf-8'

    soup = BeautifulSoup(source_response.text, 'html.parser')
    table = soup.find('table')

    for tbody_blood_banks in table.find_all('tbody'):
        rows = tbody_blood_banks.find_all('tr')

    blood_types = get_all_blood_types(rows)
    cities = get_all_cities(rows)

    for row in rows:
        bank_status.append(get_bank_status(row))

    for count_cities, city in enumerate(cities):
        blood_banks[city] = {}
        for count_bd, blood_type in enumerate(blood_types):
            blood_banks[city][blood_type] = bank_status[count_bd][count_cities]
    
    output_json = {
        "datetime_modified": get_datetime_modified(soup),
        "url_src": source_response.url,
        "blood_banks": blood_banks
    }

    print("Output JSON:\n", json.dumps(output_json, indent=2, ensure_ascii=False))
    print("Posting to API (", api_url, ")...")
    post_to_api(output_json, api_token)

if __name__ == "__main__":
    main()
