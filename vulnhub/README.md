# vulnhub-scraper

Downloads all metadata on each item from vulnhub.com, including description, download links, sha1 hash etc... and saves them in a json file.

## Prerequisites
* python3
* bs4

## Usage
```
python3 vulnhub-scraper.py <start page> <end page>
```
Sample output
```
memes@pepe:~/git/scrapers/vulnhub-scraper$ python3 vulnhub-scraper.py 27 28
==== Page 27  ====
Hackxor: 1
Hackademic: RTB2
Hackademic: RTB1
GameOver: 1
Exploit-Exercises: Fusion (v2)
```


