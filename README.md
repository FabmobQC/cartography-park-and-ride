# Cartography Park and Ride

Retrieval and formating of data for superset site entry.

## Process

TODO

## Data Format

Intermediary data inside ```/output``` is formatted as

    name,spaces_bikes,spaces_cars,latitude,longitude

inside of files named for the network they are a part of.

Final output data is formatted as

    network,name,spaces_bikes,spaces_cars,latitude,longitude

in ```output.csv```.

### Todo
* ARTM, CRE parsing
* Make main to get/compile all data
* Find data for gare centrale?
* Remove duplicates?

### Notes
* Data for the REM was compiled manually from [their site](https://rem.info/fr/se-deplacer/stations-du-reseau) and is available in the top level ```rem.csv``` file. It is lacking information for gare centrale.
* STL data from the [google drive](https://drive.google.com/drive/folders/1IU2LXkShVzD2UStD1h-28Y_ChmPG_x4p) is unusable without a paid for software ArcGIS. The stl site pages for parking ([here](https://stlaval.ca/reseau/transport/stationnement-payant) and [here](https://stlaval.ca/reseau/transport/stationnement-gratuit)) also offer no additional information beyond what is available from other network sites.