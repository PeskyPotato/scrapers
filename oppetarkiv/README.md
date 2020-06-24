# oppetarkiv-scraper

Downloads all programs with metadata from [Öppet arkiv](https://www.oppetarkiv.se).

## Prerequisites
Install python3 requirements
```
pip3 install -r requirements.txt
```
Install ffmpeg
```
sudo apt install ffmpeg
```

## Usage
```
$ python3 oppetarkiv.py -h
usage: oppetarkiv.py [-h] [-o OUTPUT]

Archive all programs from Öppet arkiv

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Set download directory
```