import requests
import os
import pandas as pd
import openpyxl
from time import sleep

os.makedirs('temp', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Get car/bike parking data files
car_parking_request = requests.get('https://drive.google.com/uc?export=download&id=1-f6-_iY47NYpyEADvOaHZEuvzLrxRkMS')
with open('temp/artm_car_parking.xlsx', 'wb') as f:
    f.write(car_parking_request.content)
sleep(0.2)
bike_parking_request = requests.get('https://drive.google.com/uc?export=download&id=1thVhqBDwxqDsaPySbb7K9LkRnkfdBkqa')
with open('temp/artm_bike_parking.xlsx', 'wb') as f:
    f.write(bike_parking_request.content)

# Load parking data files
car_parking_df = pd.read_excel('temp/artm_car_parking.xlsx')
bike_parking_df = pd.read_excel('temp/artm_bike_parking.xlsx')

# Filter down useful columns
car_parking_df = car_parking_df.filter(items=['Nom du stationnement', 'Type de case', 'Capacité'])
bike_parking_df = bike_parking_df.filter(items=['Site', 'Type_support', 'Capacite'])

# Filter out irrelevant data
car_ignorable_types = ['Illégaux', 'illégaux', 'Réservés', 'Communauto', 'Taxi']
bike_ignorable_types = ['BIXI']
car_parking_df = car_parking_df[~car_parking_df['Type de case'].isin(car_ignorable_types)]
car_parking_df = car_parking_df[car_parking_df['Capacité'].notnull()]
car_parking_df = car_parking_df[car_parking_df['Capacité'] != 0]
car_parking_df = car_parking_df.filter(items=['Nom du stationnement', 'Capacité'])
bike_parking_df = bike_parking_df[~bike_parking_df['Type_support'].isin(bike_ignorable_types)]
bike_parking_df = bike_parking_df[bike_parking_df['Capacite'].notnull()]
bike_parking_df = bike_parking_df[bike_parking_df['Capacite'] != 0]
bike_parking_df = bike_parking_df.filter(items=['Site', 'Capacite'])

# Clean names
car_parking_df['Nom du stationnement'] = (car_parking_df['Nom du stationnement']
                                          .apply(lambda x: x.lower().strip()))
bike_parking_df['Site'] = (bike_parking_df['Site']
                           .apply(lambda x: x.lower().strip()))

# TODO manually collect all coords needed
# TODO ignore data already present in other sets?
