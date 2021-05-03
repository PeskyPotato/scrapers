# wallhaven-scraper

Downloads all available images based on your search query.

## Prerequisites
* python3
* bs4

## Usage
```
usage: wallhaven-scraper.py [-h] [--sort SORT] [-o OUTPUT] query

positional arguments:
  query                 enter serach term

optional arguments:
  -h, --help            show this help message and exit
  --sort SORT           suported keywords relevance, random, date_added, views,
                        favorites, toplist
  -o OUTPUT, --output OUTPUT
                        Set download directory
```


Sample output
```bash
$ python3 wallhaven-scraper.py "forza m3" --sort date_added
Searching for forza m3
==== Page 1 ====
Karna https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-761266.png
Karna https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-761265.png
Karna https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-760423.png
asandhu23 https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-760275.jpg
jinhang https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-758660.jpg

```

## Todo
[X] Add support for sorting
[-] Add support for order
[-] Choose categories
[-] Add support for colors
[-] Add support for ratio
[-] Add support for purity (SFW/Sketchy)
[-] Add support for resolution


