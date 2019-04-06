from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from urllib.error import HTTPError
from time import sleep
import os
import sys

def scrape():

    page = 1
    while(1):
        print("==== Page", page, " ====")
        url = "http://www.impawards.com/alpha{}.html".format(page)

        req = Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

        try:
            uClient = urlopen(req)
            page_html = uClient.read()
            uClient.close()
        except HTTPError:
            print("Complete")
            break
        page_soup = soup(page_html, "lxml")

        posters = page_soup.findAll("div", {"class": "constant_thumb"})

        for poster in posters:
            src = poster.center.a.img["src"]
            name = poster.div.text
            print(name)
            urlretrieve("http://www.impawards.com{}".format(src), "posters/{}-{}".format(name.replace(" ", "_"), src.split("/")[-1]))
        page += 1


if not os.path.exists('posters'):
    os.makedirs('posters')

scrape()