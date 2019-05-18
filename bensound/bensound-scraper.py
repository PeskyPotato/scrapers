from time import sleep
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup as soup
import re
import os
import json
import sys

def scrape(category, first, last):

    for page in range(first, last):
        if category == "":
            url = "https://www.bensound.com/royalty-free-music/{}".format(page)
        else:
            url = "https://www.bensound.com/royalty-free-music/{}/{}".format(category, page)

        req = Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
        )

        uClient = urlopen(req)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "lxml")
        blocs = page_soup.find_all("div", {"class": "bloc_cat"})
        blocs = blocs[0].find_all("div", {"class": re.compile('^bloc_[a-zA-z1]*')})
        for bloc in blocs:
            url_mp3 = bloc.find_all("audio")
            if len(url_mp3) > 0:
                url_mp3 = url_mp3[0]["src"]
                print(url_mp3)
        sleep(1)


def main():
    if len(sys.argv) != 3:
        sys.exit("Specify <first page> <last page>")
    try:
        first = int(sys.argv[1])
        last = int(sys.argv[2])
    except ValueError:
        sys.exit("Only use integers")

    if first > last:
        sys.exit("Don't be stupid")

    scrape("", first, last + 1)

main()