# WAD-Archive scraper

This program is able to download all WADs from discs from [wad-archive.com](https://wad-archive.com) along with the metadata.

## Prerequisites
* python3
* python3-lxml

Install python3 requirements
```
pip3 install -r requirements.txt
```

## Usage
### All available arguments
```bash
$ python3 wad-archive-scraper.py -h
usage: wad-archive-scraper.py [-h] [-o OUTPUT] [-v]

Archive assets from wad-archive.com

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Set download directory
  -v, --verbose
```

