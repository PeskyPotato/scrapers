# unicode-emoji-chart-scraper

Downloads all Emoji with unicode, and CLDR short name into an sqlite database. All Emoji's are taken from [unicode.org](https://unicode.org/emoji/charts/full-emoji-list.html).

## Prerequisites
* python3
* bs4

## Usage
```console
python3 unicode-emoji-chart-scraper.py
```
Sample output
```
memes@pepe:~/git/scrapers/unicode-emoji-chart$ python3 unicode-emoji-chart-scraper.py
 Symbols                         
Symbols -> transport-sign
Symbols -> transport-sign U+1F3E7 🏧 ATM sign
Symbols -> transport-sign U+1F6AE 🚮 litter in bin sign
Symbols -> transport-sign U+1F6B0 🚰 potable water
Symbols -> transport-sign U+267F ♿ wheelchair symbol
Symbols -> transport-sign U+1F6B9 🚹 men’s room
Symbols -> transport-sign U+1F6BA 🚺 women’s room    
```


