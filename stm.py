import requests
import os
from time import sleep
from bs4 import BeautifulSoup

os.makedirs('network-data', exist_ok=True)

# Coordinates for stations
station_coords = {
    'Acadie': '45.52342178789101,-73.62366174510186',
    'Angrignon': '45.44635250491937,-73.60378374593185',
    'Beaubien': '45.53547635587862,-73.60458950277219',
    'Cadillac': '45.57691031940034,-73.54667190277048',
    'Cartier': '45.56023233766228,-73.68173137393575',
    'Champ-de-Mars': '45.510266213513894,-73.55658250760808',
    'Charlevoix': '45.47831001934155,-73.56938230359336',
    'Côte Sainte-Catherine': '45.492503180544844,-73.63276858927983',
    'Côte-des-Neiges': '45.49695025604521,-73.62339373160897',
    'Côte-Vertu': '45.513993660346976,-73.68295054510226',
    'Crémazie': '45.54598559194768,-73.63838167393635',
    'De Castelnau': '45.53552715347974,-73.61993737578412',
    'De la Concorde': '45.560752330203066,-73.70972151811236',
    'De la Savane': '45.500459769376995,-73.66164840462075',
    'De l\'Église': '45.46184334652256,-73.5675206046223',
    'D\'Iberville': '45.5527966226305,-73.60260190461875',
    'Du Collège': '45.509516120465534,-73.67462715859654',
    'Édouard-Montpetit': '45.51035564683521,-73.61254503160855',
    'Fabre': '45.5466743081714,-73.60805508743029',
    'Frontenac': '45.533323443093074,-73.55217893160754',
    'Georges-Vanier': '45.48895422101163,-73.57646855859736',
    'Henri-Bourassa': '45.556170545264564,-73.6673000585946',
    'Honoré-Beaugrand': '45.59691748297711,-73.5344837469463',
    'Jarry': '45.543309840184456,-73.62831005859506',
    'Jean-Talon': '45.539763663836894,-73.61367400277193',
    'Jolicoeur': '45.45682187675068,-73.5820551316106',
    'Joliette': '45.54713924851065,-73.55151160277163',
    'Langelier': '45.58284109533651,-73.5430042567462',
    'Lasalle': '45.47087648558098,-73.5662036757867',
    'L\'Assomption': '45.56947127373298,-73.54678981811206',
    'Laurier': '45.52716206896813,-73.58651513160775',
    'Lionel-Groulx': '45.48290977112258,-73.57988164879816',
    'Lucien-L\'Allier': '45.495081035889314,-73.57097691811505',
    'Monk': '45.45125481498726,-73.59321754510478',
    'Montmorency': '45.55852920153009,-73.7215576604418',
    'Mont-Royal': '45.524654537558064,-73.5817148181139',
    'Namur': '45.49504553592743,-73.65292181626772',
    'Outremont': '45.52019091258359,-73.61493816044333',
    'Papineau': '45.523822122563885,-73.55217649112588',
    'Parc': '45.530514851127904,-73.62387442420523',
    'Pie-IX': '45.55375551136834,-73.5517687459011',
    'Place-Saint-Henri': '45.477118840069956,-73.58654494695104',
    'Place-d\'Armes': '45.50583056900168,-73.55996214776216',
    'Place-des-Arts': '45.507888816691114,-73.5688025739379',
    'Plamondon': '45.49440544482878,-73.63796687475339',
    'Préfontaine': '45.5416099581183,-73.55429695859516',
    'Radisson': '45.58955960671167,-73.53924654509927',
    'Rosemont': '45.53127469720959,-73.59776737393695',
    'Saint-Laurent': '45.5109116189744,-73.56481434510248',
    'Saint-Michel': '45.559951790421984,-73.59994614510046',
    'Sauvé': '45.55075901588006,-73.65610038743019',
    'Sherbrooke': '45.518375328492226,-73.56823673160801',
    'Square-Victoria-OACI': '45.50203572685435,-73.56309654510282',
    'Université-de-Montréal': '45.502779736433105,-73.61832322365659',
    'Vendôme': '45.473939883695365,-73.60379361303292',
    'Verdun': '45.45925024722524,-73.57171686044575',
    'Viau': '45.56119028284351,-73.54725626044174',
    'Villa-Maria': '45.479641197718905,-73.61977087393895',
}

# Get bike parking spots
stm_bike_parking = {}
bike_parking_request = requests.get('https://www.stm.info/fr/velo/bienvenue-aux-velos')
bike_parking_soup = BeautifulSoup(bike_parking_request.text, 'html.parser')
parking_table_rows = bike_parking_soup.find('table').find_all('tr')
for table_row in parking_table_rows:
    table_data = table_row.find_all('td')
    if len(table_data) == 2:
        stm_bike_parking[table_data[0].text.strip()] = table_data[1].text.strip()

# Get station coordinates
stm_data = []
for key, value in stm_bike_parking.items():
    coordinates = station_coords[key]
    stm_data.append(f"{key},{value},0,{coordinates}")

with open('network-data/stm.csv', 'w') as f:
    for entry in stm_data:
        f.write(f"{entry}\n")
