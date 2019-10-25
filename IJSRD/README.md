# IJSRD-scraper

Downloads papers published to [International Journal for Scientific Research & Development](http://ijsrd.com).

## Prerequisites

* python3
* bs4
* requests
* html5lib

## Usage

```
python3 IJSRD-scraper.py
```

## Additional Information

The archives are divided into volumes and issues with each page displaying 50 papers. The link is structured in this fashion, here is the url for volume 1, issue 1 on the second page (offset 50).

```
http://ijsrd.com/index.php?p=Archive&v=1&i=1&start=50
```

The PDF urls are structured like so
```
http://www.ijsrd.com/articles/IJSRDV1I1001.pdf
http://www.ijsrd.com/articles/IJSRDV3I80519.pdf
http://www.ijsrd.com/articles/IJSRDV3I90254.pdf
```

A side note, I usually use `lxml` to parse the html from the webpages  scrape. In this instance, it did not get all the table elements, or on some pages didn't parse the table at all. So I came across this [useful StackOverflow answer](https://stackoverflow.com/questions/18614305/missing-parts-on-beautiful-soup-results) that suggested using `html5lib` for the exact same problem. Worked like a charm.