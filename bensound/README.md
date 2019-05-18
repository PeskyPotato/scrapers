# bensound-scraper

Downloads all the books from memoryoftheworld.org.

## Prerequisites
* python3 
* bs4

## Usage
To list out all the mp3 links
```
python3 bensound-scraper.py <start page> <end page>
```
If you wish to download the files as the scripts lists them you can pipe them into wget using xargs.

```
python3 bensound-scraper.py <start page> <end page> | xargs -n1 wget
```

Sample output
```
memes@pepe:~/git/scrapers/bensound-scraper$python3 bensound-scraper.py 1 10
https://www.bensound.org/bensound-music/bensound-summer.mp3
https://www.bensound.org/bensound-music/bensound-ukulele.mp3
https://www.bensound.org/bensound-music/bensound-creativeminds.mp3
https://www.bensound.org/bensound-music/bensound-anewbeginning.mp3
```

If you wish to list files from just a specific category pass in the string as the first parameter of scrape in line 55. Valid categories are
* "acounstic-folk"
* "cinematic"
* "corporate-pop"
* "electronica"
* "urban-groove"
* "jazz"
* "rock"
* "world-others"
