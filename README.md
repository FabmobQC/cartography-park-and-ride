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
* ARTM parsing
* Make main to get/compile all data
* Find data for gare centrale?
* Remove duplicates?

### Notes
* Data for the REM was compiled manually from [their site](https://rem.info/fr/se-deplacer/stations-du-reseau) and is available in the top level ```rem.csv``` file. It is lacking information for gare centrale.
* STL data from the [google drive](https://drive.google.com/drive/folders/1IU2LXkShVzD2UStD1h-28Y_ChmPG_x4p) is unusable without a paid for software ArcGIS. The STL site pages for parking ([here](https://stlaval.ca/reseau/transport/stationnement-payant) and [here](https://stlaval.ca/reseau/transport/stationnement-gratuit)) also offer no additional information beyond what is available from other network sites.
* [CRE data](https://drive.google.com/drive/folders/1RZmOJlr1fguQiUzg8Hwif7lIYvBHDwbS) was extracted from the kml (the kmz is identical and the geojson is just a subset of the data). Data was filtered down to only be that which includes the string "incitatif" as there was a significant amount of other irrelevant data, like commercial parking.
* When necessary, coordinates for addresses/stations were retrieved manually and placed in script as there is no free stable api available for geocoding.
