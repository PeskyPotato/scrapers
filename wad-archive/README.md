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
usage: wad-archive-scraper.py [-h] [-p PROCESSES]

Archive documents from riksdagen.se

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSES, --processes PROCESSES
                        Set number of concurrent downloads
```

## Notes
Downloading requires you to sign in, so after you sign in export the `cookies.txt` file and place it in the same directory as the scraper. The file must be called `cookies.txt`.