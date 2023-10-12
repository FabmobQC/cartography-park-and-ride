# Cartography Park and Ride

Retrieval and formating of data for superset site entry.

## Process

Data for the REM compiled manually from https://rem.info/fr/se-deplacer/stations-du-reseau

## Data Format

Intermediary data inside ```/output``` is formatted as

    name,spaces_bikes,spaces_cars,latitude,longitude

inside of files named for the network they are a part of.

Final output data is formatted as

    network,name,spaces_bikes,spaces_cars,latitude,longitude

in ```output.csv```.

### Todo
* STL crosscheck and parsing
* ARTM, RTL, CRE parsing
* Make main to get/compile all data
* Find data for gare centrale?
* Remove duplicates?