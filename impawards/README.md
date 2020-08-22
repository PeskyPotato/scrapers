# impaward-scraper

Downloads all available movie posters from [IMP Awards](http://www.impawards.com/)

## Prerequisites
Install python3 requirements
```
pip3 install -r requirements.txt
```

## Usage
### All available arguments
```bash
$ python3 impawards-scraper.py -h
usage: impawards-scraper.py [-h] [--start START] [--end END] [-o OUTPUT]

Archive posters from impawards.com

optional arguments:
  -h, --help            show this help message and exit
  --start START         Starting pages number
  --end END             Ending page number
  -o OUTPUT, --output OUTPUT
                        Set download directory

```

### Downloads all available posters
```
python3 impawards-scraper.py 
```

### Downloads a range from alphabetically
The pages can be viewed on the [site](http://www.impawards.com/alpha1.html).
```bash
$ python3 impawards-scraper.py --start 1 --end 10
```

