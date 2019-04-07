# thecoverproject-scraper

Downloads all available game posters from TheCoverProject.

## Prerequisites
* python3
* bs4

## Usage
To download all the available cover ids enter the following.
```
python3 thecoverproject-scraper.py 
```

Any cover_ids that failed to download will be entered in the `error.log` file. The following ids are known to be missing from the site `[1, 2, 5, 3, 1847, 2021, 7063, 7644, 9794, 10347, 9361]` and `[946, 9361]` only have their thumbnails available. If any other cover_id appears in the log file you can retry downloading them by simply using the --id flag, like below, this will only download the cover_id 835.
```
python3 thecoverproject-scraper.py --id 835
```

Sample output
```
memes@pepe:~/git/scrapers/thecoverproject$ python3 thecoverproject-scraper.py
1 007: The World is Not Enough Nintendo 64
7 Aero Gauge Nintendo 64
4 1080 Snowboarding Nintendo 64
10 All Star Baseball '99 Nintendo 64
13 Army Men Air Combat Nintendo 64
```

