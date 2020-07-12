# Riksdagen scraper

This program is able to download debates from [Riksdagen.se](https://riksdagen.se/sv/webb-tv) along with the metadata.

## Prerequisites
Install python3 requirements
```
pip3 install -r requirements.txt
```

## Usage
### All available arguments
```bash
$ python3 riksdagen.py -h
usage: riksdagen.py [-h] [--start START] [--end END] [--update UPDATE]
                    [-o OUTPUT]

Archive debates from riksdagen.se

optional arguments:
  -h, --help                    show this help message and exit
  --start START                 Starting page
  --end END                     Ending page
  --update UPDATE               Year (2XXX) or all
  -o OUTPUT, --output OUTPUT    Set download directory
```

### Download all available programs
Note that doing this will take a considerable amount of time to iterate through all the pages and years to collect the data required to start the video downloads. 
```bash
$ python3 riksdagen.py --update all
```

### Download from a specific year
This will download debates from from the end of 2019 to the beginning of 2020, in other words debates listed [here](https://riksdagen.se/sv/webb-tv/?riksmote=2019/20). If you wish to start or end on a specific use `--start <int>` or `--end <int>` respectively replacing `<int>` with your desired page.
```bash
$ python3 riksdagen.py --update 2019
```

### Download all documents
This downloads all available documents in html and sql form from [http://data.riksdagen.se/data/dokument/](http://data.riksdagen.se/data/dokument/) and divides them into folders. 
```bash
$ python3 dokument.py
```
$ python3 dokument.py -h
Optional parameters for `dokument.py.
```bash
usage: dokument.py [-h] [-o OUTPUT] [-p PROCESSES]

Archive documents from riksdagen.se

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Set download directory
  -p PROCESSES, --processes PROCESSES
                        Set number of concurrent downloads
```