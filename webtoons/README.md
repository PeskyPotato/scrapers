# webtoons-scraper

Downloads webtoons and organises them by episode/chapter.

## Prerequisites
* python3
* beautifulsoup4
* requests

## Usage
Pass in a url from the episode/chapter viewer, you can also specify the start and stop episodes/chapters. If these do not exist the scraper will attempt to download all available content from the series.
```bash
$ python3 webtoons-scraper.py "https://www.webtoons.com/en/fantasy/tower-of-god/season-2-ep-131/viewer?title_no=95&episode_no=50"
```
Optional flags:
  --start START  Starting chapter
  --end END      Ending chapter

Sample output
```bash
$ python3 webtoons-scraper.py "https://www.webtoons.com/en/fantasy/tower-of-god/season-2-ep-131/viewer?title_no=95&episode_no=50" --start 1 --end 5
1 --- season-1-ep-0
tower-of-god: season-1-ep-0 - total time: 0.96s
2 --- season-1-ep-1-1fheadons-floor
tower-of-god: season-1-ep-1-1fheadons-floor - total time: 3.98s
3 --- season-1-ep-2
tower-of-god: season-1-ep-2 - total time: 7.66sonds
4 --- season-1-ep-3
```
