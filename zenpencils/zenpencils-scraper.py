from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import os
import sys
import time

def scrape():
    dir = os.path.dirname(os.path.abspath(__file__))
    zendir = os.path.join(dir, "ZenComics")

    if not os.path.exists(zendir):
            os.makedirs(zendir)

    count = 0
    while(1):
        main_url = "http://zenpencils.com/comic/" + str(count)
        headers = {'User-agent': 'Mozilla/5.0'}

        main_url_opener = urlopen(main_url)
        try:
            main_url_response = main_url_opener.read()

            main_url_soup = BeautifulSoup(main_url_response,"lxml")
            images = main_url_soup.findAll("div", {"id": "comic"})
            image = images[0].img['src']
            name = image.split('/')[-1]
            print("Downloading", name)
            open_image = urlopen(image)
            image_data = open_image.read()
            with open(os.path.join(zendir, name), 'wb') as f:
                f.write(image_data)
        except HTTPError:
            print ("Complete: " + str(count) + " images downloaded.")
            break
        count += 1


def main():
    scrape()

main()