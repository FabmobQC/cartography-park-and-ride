import requests
import lxml
import os
import re
from bs4 import BeautifulSoup
from zipfile import ZipFile

os.makedirs('temp', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Get parking data files
parking_request = requests.get('https://drive.google.com/uc?export=download&id=1cijwGauU5txVTaRO3vR6vS3hI7NhSBiw')
with open('temp/rtl_parking.kmz', 'wb') as f:
    f.write(parking_request.content)

# Extract kml file
with ZipFile('temp/rtl_parking.kmz', 'r') as f:
    f.extractall('temp')

# Read in kml data
soup = {}
with open('temp/doc.kml', 'r') as f:
    soup = BeautifulSoup(f.read(), 'xml')

# Parse placemark parking data
placemarks = soup.find_all('Placemark')
parking_data = ''
for placemark in placemarks:
    name = placemark.find('name').text.strip()
    coords = placemark.find('coordinates').text.strip().split(',')
    lat = coords[1]
    long = coords[0]
    description_lines = placemark.find('description').text.split('<br>')
    bike_parking = 0
    car_parking = 0
    for description_line in description_lines:
        if description_line.startswith('Nombre de supports'):
            numbers = re.findall(r'\d+', description_line)
            if len(numbers) != 0:
                bike_parking = int(numbers[0])
        elif description_line.startswith('Support pour vélo'):
            numbers = re.findall(r'\d+', description_line)
            if len(numbers) != 0:
                bike_parking = int(numbers[0])
        elif (description_line.startswith('Stationnement gratuit')
                or description_line.startswith('Stationnement payant')):
            numbers = re.findall(r'\d+', description_line)
            if len(numbers) != 0:
                car_parking += int(numbers[0])
    parking_data += f"{name},{bike_parking},{car_parking},{lat},{long}\n"

# Write parking data to file
with open('output/rtl.csv', 'w') as f:
    f.write(parking_data)
