# memoryofthewolrd-scraper

Downloads all the metadata for the books on memoryoftheworld.org and creates `books.txt` with direct links to all the books. This text file can be passed into `wget` to download all the books.

## Prerequisites
* python3 

## Usage
```console
python3 memoryoftheworld-scraper.py <start_page> <end_page>
```
For example to download only the first page
```console
memes@pepe:~/git/scrapers/memoryoftheworld-scraper$ python3 memoryoftheworld-scraper.py 1 1
```
