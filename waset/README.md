# waset-scraper

Downloads papers published to the popular predatory publisher waset.org :)

## Prerequisites
* python3
    * bs4
* parallel
* wget

## Usage

Get all the PDF and JSON file urls into a text file. This will take some time.

```
python3 waset-scraper.py > urls.txt
```

After that is complete you can then download the files in parallel.

```
cat urls.txt | parallel -j10 {}
```
