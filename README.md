# py4qualar
python scripts to analyze portuguese air quality data downloaded from http://qualar.apambiente.pt/

Data has to be previously downloaded from http://qualar.apambiente.pt/ "Dados de todas as estações para um poluente num dado ano" (downloads one file per pollutant and per year containing hourly concentrations observed at all the Portuguese air quality network sites).
The file read_qualar.py reads the downloaded files and stores the data as a Pandas DataFrame (one DataFrame per pollutant).
