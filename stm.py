import requests
import os
from time import sleep
from bs4 import BeautifulSoup

os.makedirs('output', exist_ok=True)

# Get bike parking spots
stm_bike_parking = {}
bike_parking_request = requests.get('https://www.stm.info/fr/velo/bienvenue-aux-velos')
bike_parking_soup = BeautifulSoup(bike_parking_request.text, 'html.parser')
parking_table_rows = bike_parking_soup.find('table').find_all('tr')
for table_row in parking_table_rows:
    table_data = table_row.find_all('td')
    if len(table_data) == 2:
        stm_bike_parking[table_data[0].text.strip()] = table_data[1].text.strip()

# Link variations for stations
station_links = {
    'Cartier': 'cartier-(zone-b)',
    'De la Concorde': 'de-la-concorde-(zone-b)',
    'L\'Assomption': 'Assomption',
    'Montmorency': 'montmorency-(zone-b)'
}

# Coordinates for missing stations
station_coords = {
    'Côte-des-Neiges': '45.4959034,-73.6242076'
}

# Get station coordinates
stm_data = []
for key, value in stm_bike_parking.items():
    sleep(0.2)
    coordinates = ''
    if key in station_coords:
        coordinates = station_coords[key]
    else:
        station_request = {}
        if key in station_links:
            station_request = requests.get(f"https://www.stm.info/fr/infos/reseaux/metro/{station_links[key]}")
        else:
            suffix = key.replace('\'', '-').replace(' ', '-')
            station_request = requests.get(f"https://www.stm.info/fr/infos/reseaux/metro/{suffix}")
        station_soup = BeautifulSoup(station_request.text, 'html.parser')
        map_link = station_soup.find('div', {'class': 'editor'}).find('iframe')
        long = map_link.get('src').strip().split('?')[1].split('=')[1].split('!')[5].lstrip('2d')
        lat = map_link.get('src').strip().split('?')[1].split('=')[1].split('!')[6].lstrip('3d')
        coordinates = f"{lat},{long}"
    stm_data.append(f"{key},{value},0,{coordinates}")

with open('output/stm.csv', 'w') as f:
    for entry in stm_data:
        f.write(f"{entry}\n")
