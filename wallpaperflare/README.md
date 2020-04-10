# wallpaperflare-scraper

Download all, or some wallpapers through search terms and page limits from wallpaperflare.com.

## Prerequisites 
* python3
* requests
* bs4

## Usage
To scrape all wallpapers from Wallpaper Flare:
```console
python3 wallpaperflare-scraper.py
```

To set the start, end or search term use the following flags.
```console
  -h, --help                 show this help message and exit
  --start START              Starting page
  --end END                  Ending page
  --search_term SEARCH_TERM  Search term
```
