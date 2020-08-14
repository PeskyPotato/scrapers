# Smutbase scraper

This program is able to download all assets from [Smutba.se](https://smutba.se) along with the metadata, this site is NSFW.

## Prerequisites
Install python3 requirements
```
pip3 install -r requirements.txt
```

## Usage
### All available arguments
```
usage: smutbase-scraper.py [-h] [--start START] [--end END] [-o OUTPUT]

Archive assets from Smutbase

optional arguments:
  -h, --help            show this help message and exit
  --start START         Starting project ID
  --end END             Ending project ID
  -o OUTPUT, --output OUTPUT
                        Set download directory
```

### Download all available assets
```bash
$ python3 smutbase-scraper.py
```

### Download a range
```bash
$ python3 smutbase-scraper.py --start 1 --end 10
```
