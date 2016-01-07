# NFL DATA SCRAPER

This script extracts NFL Fantasy data from http://fantasy.nfl.com/research and streams it as csv data and can be piped to a text file as shown in the usage section. At the moment the script only extracts one position's game of a specific week of the season. Once the datasets are extracted into CSV files they can be used for fantasy analysis using MS Excel, SQL, etc....

I'm constantly working on the script to clean it up and add more features. 

## Usage:
This script was built with BeautifulSoup (3.2.1) and needs to be installed on the system where the script will be running.

To scrap all Wide Reciever data for the 2015 season for week 2 the script should be executed as shown below.

```os
./get_nfl_data.py -y 2015 -w 2 -p wr > WR_2015_2.csv
```

To see details of arguments the script accepts use help:
```os
./get_nfl_data.py --help
```
