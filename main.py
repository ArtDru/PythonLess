import requests
from bs4 import BeautifulSoup
import lxml
import json

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

festival_url_list = []
for i in range(0, 24, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=17%20Apr%202022&to_date=&genre%5B%5D=pop&maxprice=500&o={i}&bannertitle=July"
    print(url)
    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data['html']

    with open(f"data/index_{i}.html", "w") as file:
        file.write(html_response)

    with open(f"data/index_{i}.html") as file:
        html_response = file.read()

    soup = BeautifulSoup(html_response, 'lxml')
    cards = soup.find_all('a', class_='card-details-link')

    for item in cards:
        fest_url ="https://www.skiddle.com/" + item.get('href')
        festival_url_list.append(fest_url)

count = 0
fest_result = []
for url in festival_url_list:
    req = requests.get(url=url, headers=headers)
    count += 1
    print(count)
    print(url)

    try:
        soup = BeautifulSoup(req.text, 'lxml')
        fest_info_block = soup.find('div', class_='top-info-cont')
        fest_name = fest_info_block.find('h1').text.strip()
        fest_data = fest_info_block.find('h3').text.strip()
        fest_location_url = "https://www.skiddle.com/" + fest_info_block.find('a', class_='tc-white').get('href')

        # req = requests.get(url=fest_location_url, headers=headers)
        # soup = BeautifulSoup(req.text, 'lxml')

        fest_result.append({
            "fest_name": fest_name,
            "fest_data": fest_data,
            "fest_location": soup.find('h1').text.strip(),

        })

    except Exception as ex:
        print(ex)
        print("error")

with open(f"data/fest_result.json", "a", encoding="utf-8" ) as file:
    json.dump(fest_result, file, indent=4, ensure_ascii=False)

