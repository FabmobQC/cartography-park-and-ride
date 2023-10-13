import requests
import lxml
import re
import os
from bs4 import BeautifulSoup

os.makedirs('output', exist_ok=True)

# Manually retrieved coordinates for the final data which only had an address
ADDRESS_COORDINATES = {
    '1200 Rue Lenoir Saint-Bruno-de-Montarville': '45.5133054,-73.3766342',
    '1895 avenue PANAMA Brossard': '45.5133054,-73.3766342',
    '101 Rue Mercier Saint-Lambert': '45.5133054,-73.3766342',
    '260 boul. DE MONTARVILLE Boucherville': '45.5133054,-73.3766342',
    '1200 rue AMPÈRE Boucherville': '45.5133054,-73.3766342',
    '4812 Route de l\'Aéroport Longueuil': '45.5133054,-73.3766342',
    '2505 Rue Patrick Saint-Hubert': '45.5078882,-73.4383666',
    '180, ARMAND-FRAPPIER BOULEVARD Sainte-Julie': '45.5827585,-73.328622',
    '170 rue Saint-Laurent Beauharnois': '45.3143105,-73.8832422',
    '555 Rue Boîleau Vaudreuil-Dorion': '45.3999709,-74.0544742',
    '10 boulevard Perrot L\'Île-Perrot': '45.3959767,-73.9661289',
    '3001 Boulevard Fréchette Chambly': '45.4328666,-73.3036244',
    '121 Rue de la Gare Saint-Basile-le-Grand': '45.5235463,-73.3079311',
    '399 Rue du Purvis Club McMasterville': '45.5457061,-73.2337543',
}

# Get parking kml
parking_request = requests.get('https://drive.google.com/uc?export=download&id=1RkYjiLyd-cLI5_HmGhHGh1neOJW9UR-Q')
parking_kml = BeautifulSoup(parking_request.text, 'xml')

# Filter and build parking data
placemarks = parking_kml.find_all('Placemark')
parking = ''
for placemark in placemarks:
    if 'incitatif' in placemark.text.lower():
        capacity_element = placemark.find('Data', {'name': 'Capacité'})
        places_element = placemark.find('Data', {'name': 'Places'})
        coordinates_element = placemark.find('coordinates')
        name = placemark.find('name').text.strip()
        spots = 0
        if capacity_element is not None:
            numbers = re.findall(r'\d+', capacity_element.text.strip())
            if len(numbers) != 0:
                spots = numbers[0]
        elif places_element is not None:
            numbers = re.findall(r'\d+', places_element.text.strip())
            if len(numbers) != 0:
                spots = numbers[0]
        if spots != 0:
            if coordinates_element is not None:
                coordinates = coordinates_element.text.strip().split(',')
                parking += f"{name},0,{spots},{coordinates[1]},{coordinates[0]}\n"
            else:
                address = placemark.find('address').text.strip()
                parking += f"{name},0,{spots},{ADDRESS_COORDINATES[address]}\n"

# Write parking data to file
with open('output/cre.csv', 'w') as f:
    f.write(parking)
