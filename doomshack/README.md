# Doomshack scraper

This program is able to save a text file for all wad and zip urls from [Doomshack](https://doomshack.org/).

## Prerequisites
Install python3 requirements
```
pip3 install -r requirements.txt
```

## Usage
### All available arguments
```
usage: doomshack-scraper.py [-h] [--files FILES] [--type TYPE]

Get list of file urls from doomshack.org

options:
  -h, --help     show this help message and exit
  --files FILES  Total number of files
  --type TYPE    Type of file, zip or wad
```
### Default values
Up to 10000 file urls will be requested of type "wad". Use `--files` or `--type` to adjust these values.
```
python doomshack-scraper.py
```