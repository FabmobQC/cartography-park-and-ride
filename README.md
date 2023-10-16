# Cartography Park and Ride

Retrieval and formating of data for superset site entry.

## Process

1. Run the ```artm.py```, ```cre.py```, ```exo.py```, ```rtl.py```, and ```stm.py``` scripts as needed for each network's data to be generated in ```/network-data```.
2. Add any other manual data into the network-data directory for it to be parsed (as the ```rem.csv```). Be sure it respects the below formatting.
3. Run ```main.py```.
4. Manually evaluate and remove possible duplicates based on script warnings.

## Data Format

Network data inside ```/network-data``` is formatted as

    name,spaces_bikes,spaces_cars,latitude,longitude

inside of files named for the network they are a part of.

Final output data is formatted as

    network,name,spaces_bikes,spaces_cars,latitude,longitude

in ```output.csv```.

### Notes
* Data for the REM was compiled manually from [their site](https://rem.info/fr/se-deplacer/stations-du-reseau) and is available in the ```rem.csv``` file. It is lacking information for gare centrale.
* STL data from the [google drive](https://drive.google.com/drive/folders/1IU2LXkShVzD2UStD1h-28Y_ChmPG_x4p) is unusable without a paid for software ArcGIS. The STL site pages for parking ([here](https://stlaval.ca/reseau/transport/stationnement-payant) and [here](https://stlaval.ca/reseau/transport/stationnement-gratuit)) also offer no additional information beyond what is available from other network sites.
* [CRE data](https://drive.google.com/drive/folders/1RZmOJlr1fguQiUzg8Hwif7lIYvBHDwbS) was extracted from the kml (the kmz is identical and the geojson is just a subset of the data). Data was filtered down to only be that which includes the string "incitatif" as there was a significant amount of other irrelevant data, like commercial parking.
* When necessary, coordinates for addresses/stations were retrieved manually and placed in script as there is no free stable api available for geocoding.
* The EXO and STM scripts may take a few minutes as they have to make many requests to fetch their data.

### Duplicates

The following are duplicates that were present across the compiled data.
Those which are crossed out were discarded manually after being compiled with the main script.

* **anjou**: EXO, ~~ARTM~~
* **radisson**: RTL, ~~ARTM, STM~~
* **rivière-des-prairies**: EXO, ~~ARTM~~
* **saint-léonard**: EXO, ~~ARTM~~
* **pointe-aux-trembles**: EXO, ~~ARTM~~
* **sainte-thérèse**: EXO, ~~ARTM~~
* **touraine**: ARTM, ~~RTL~~
* **seigneurial**: RTL, ~~ARTM~~
* **panama**: REM, ~~ARTM, CRE, RTL~~
* **namur**: ARTM, ~~STM~~
* **cartier**: ARTM, ~~STM~~
* **chevrier**: RTL, ~~ARTM~~
* **de la concorde**: EXO, ~~ARTM, STM~~
* **de montarville**: ARTM, ~~CRE, RTL~~
* **de mortagne**: ARTM, ~~CRE, RTL~~
* **longueuil-saint-hubert**: EXO, ~~ARTM, CRE, RTL~~
* **montmorency**: ARTM, ~~CRE, STM~~
* **dorval**: EXO, ~~ARTM~~
* **saint-lambert**: EXO, ~~CRE, RTL~~
* **ile-perrot**: EXO, ~~CRE~~
* **saint-basile-le-grand**: EXO, ~~CRE~~
* **mcmasterville**: EXO, ~~CRE~~
* **vaudreuil**: EXO, ~~CRE~~
* **saint-bruno**: EXO, ~~CRE, RTL~~

There was also two longueuil locations left in the RTL data that were duplicates so one was removed.
