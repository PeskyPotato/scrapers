# memoryofthewolrd-scraper

Downloads all the books from memoryoftheworld.org.

## Prerequisites
* python3 

## Usage
```
python3 memoryoftheworld-scraper.py | sed -e 's/^/"/g' -e 's/$/"/g' | xargs -n1 wget
```
Sample output
```
memes@pepe:~/git/scrapers/memoryoftheworld-scraper$python3 memoryoftheworld-scraper.py | sed -e 's/^/"/g' -e 's/$/"/g' | xargs -n1 wget
--2019-04-12 20:17:03--  https://outernationale.memoryoftheworld.org/Mirko%20Grmek/Pathological%20Realities_%20Essays%20on%20D%20(4565)/Pathological%20Realities_%20Essays%20-%20Mirko%20Grmek.pdf
```
