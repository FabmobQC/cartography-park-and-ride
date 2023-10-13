import requests
import os
import pandas as pd
import openpyxl
from time import sleep

os.makedirs('temp', exist_ok=True)
os.makedirs('network-data', exist_ok=True)

# Manually retrieved coordinates for the final data
SITE_COORDINATES = {
    'anjou': '45.6175495,-73.5959906',
    'avenue des bois': '45.5473799,-73.8273641',
    'beloeil': '45.5958525,-73.1947787',
    'chevrier': '45.4569453,-73.4416275',
    'panama': '45.4658993,-73.4714729',
    'cartier': '45.5592823,-73.681996',
    'cartier (aréna)': '45.5590989,-73.6837067',
    'de montarville': '45.6008121,-73.4509616',
    'de mortagne': '45.5723609,-73.4431919',
    'de la concorde': '45.5596956,-73.7090516',
    'deux-montagnes': '45.5448212,-73.9119832',
    'dorval': '45.447935,-73.7429091',
    'le carrefour': '45.568068,-73.747606',
    'longueuil': '45.5091826,-73.435261',
    'montmorency': '45.5574033,-73.7206144',
    'montmorency (extérieur)': '45.5574033,-73.7206144',
    'montmorency (intérieur)': '45.5574033,-73.7206144',
    'namur est': '45.4938135,-73.6544247',
    'namur ouest': '45.4931209,-73.6554441',
    'namur (est et ouest)': '45.4935271,-73.6548758',
    'pointe-aux-trembles': '45.6742703,-73.5056293',
    'radisson': '45.5901286,-73.5375959',
    'rivière-des-prairies': '45.6605691,-73.5409043',
    'roxboro-pierrefonds': '45.510595,-73.8129084',
    'sainte-dorothée': '45.5225934,-73.8626727',
    'sainte-julie': '45.5808286,-73.3295511',
    'saint-léonard': '45.5992893,-73.6172804',
    'sainte-thérèse': '45.6352691,-73.8346918',
    'saint-martin': '45.6113106,-73.6627024',
    'seigneurial': '45.5141191,-73.3457715',
    'sherbrooke est': '45.6677231,-73.5061735',
    'sunnybrooke': '45.5042129,-73.784891',
    'terrebonne': '45.6978399,-73.652771',
    'touraine-a20': '45.5708551,-73.412086',
    'varennes': '45.6727814,-73.4269963'
}

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
CAR_IGNORABLE_TYPES = ['Illégaux', 'illégaux', 'Réservés', 'Communauto', 'Taxi', 'Débarcadère']
BIKE_IGNORABLE_TYPES = ['BIXI']
car_parking_df = car_parking_df[~car_parking_df['Type de case'].isin(CAR_IGNORABLE_TYPES)]
car_parking_df = car_parking_df[car_parking_df['Capacité'].notnull()]
car_parking_df = car_parking_df[car_parking_df['Capacité'] != 0]
car_parking_df = car_parking_df.filter(items=['Nom du stationnement', 'Capacité'])
bike_parking_df = bike_parking_df[~bike_parking_df['Type_support'].isin(BIKE_IGNORABLE_TYPES)]
bike_parking_df = bike_parking_df[bike_parking_df['Capacite'].notnull()]
bike_parking_df = bike_parking_df[bike_parking_df['Capacite'] != 0]
bike_parking_df = bike_parking_df.filter(items=['Site', 'Capacite'])

# Clean names
CAR_PARKING_REPLACEMENTS = {'pointes-aux-trembles': 'pointe-aux-trembles'}
BIKE_PARKING_REPLACEMENTS = {
    'de touraine-a20': 'touraine-a20',
    'ste-dorothée': 'sainte-dorothée',
    'sainte-léonard': 'saint-léonard'
}
car_parking_df['Nom du stationnement'] = car_parking_df['Nom du stationnement'].apply(lambda x: x.lower().strip())
car_parking_df['Nom du stationnement'] = (car_parking_df['Nom du stationnement'].replace(CAR_PARKING_REPLACEMENTS))
bike_parking_df['Site'] = bike_parking_df['Site'].apply(lambda x: x.lower().strip())
bike_parking_df['Site'] = bike_parking_df['Site'].replace(BIKE_PARKING_REPLACEMENTS)

# Group parking counts
car_parking_df = car_parking_df.groupby(by=['Nom du stationnement']).sum()
bike_parking_df = bike_parking_df.groupby(by=['Site']).sum()

# Join
parking_df = car_parking_df.join(bike_parking_df, how='outer').fillna(0)

# Build parking data
parking_data = ''
for site in parking_df.itertuples():
    parking_data += f"{site[0]},{int(site[2])},{int(site[1])},{SITE_COORDINATES[site[0]]}\n"

# Write parking data
with open('network-data/artm.csv', 'w') as f:
    f.write(parking_data)
