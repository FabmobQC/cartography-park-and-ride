import requests
import os
from time import sleep
from bs4 import BeautifulSoup

os.makedirs('network-data', exist_ok=True)

# Get line page links for a single direction each
line_urls = []
lines_request = requests.get('https://exo.quebec/fr/planifier-trajet/train')
lines_soup = BeautifulSoup(lines_request.text, 'html.parser')
line_table = (lines_soup
              .find(id='LignesContenu')
              .find('ul', {'class': 'affichage_ecran'})
              .find_all('ul', {'class': 'tab_line_name'}))
for line_row in line_table:
    link = line_row.find('a')
    line_urls.append(f"https://exo.quebec{link.get('href').strip()}")

# Get line station list page links
line_station_list_urls = []
for line_url in line_urls:
    sleep(0.2)
    line_request = requests.get(line_url)
    line_soup = BeautifulSoup(line_request.text, 'html.parser')
    route_id = line_soup.find(id='routeId').get('value')
    transport_type = line_soup.find(id='transportType').get('value')
    agence_id = line_soup.find(id='agenceId').get('value')
    sens_direction = line_soup.find(id='sensDirection').get('value')
    line_station_list_urls.append(f"https://exo.quebec/Amt.Planificateur/Itineraire/ObtenirItineraire"
                                  f"?transportType={transport_type}&agenceId={agence_id}"
                                  f"&routeId={route_id}&sensDirection={sens_direction}")

# Get station links
station_urls = []
for line_station_list_url in line_station_list_urls:
    sleep(0.2)
    line_station_list_request = requests.get(line_station_list_url)
    line_stations_list_soup = BeautifulSoup(line_station_list_request.text, 'html.parser')
    line_station_links = line_stations_list_soup.find_all('a', {'class': 'route_link'})
    for line_station_link in line_station_links:
        station_urls.append(f"https://exo.quebec/{line_station_link.get('href').strip()}")

# Get station parking data
parking_data = {}
for station_url in station_urls:
    sleep(0.2)
    station_request = requests.get(station_url)
    station_soup = BeautifulSoup(station_request.text, 'html.parser')
    station_info = station_soup.find(id='InformationsGare')
    car_parking = station_info.find(id='SationnementIncitatif').find('strong').text.strip().split(' ')[0]
    if car_parking == 'Aucune':
        car_parking = 0
    bike_parking = station_info.find(id='SupportVelo').find('strong').text.strip().split(' ')[0]
    if bike_parking == 'Aucune':
        bike_parking = 0
    name = station_info.find(id='InfosGareCarte').find('img').get('alt')
    coords = station_info.find(id='InfosGareCarte').find('img').get('src').split('?')[1].split('&')[0].split('=')[1]
    parking_data[name] = f"{bike_parking},{car_parking},{coords}"
with open('network-data/exo.csv', 'w') as f:
    for key, value in parking_data.items():
        f.write(f"{key},{value}\n")