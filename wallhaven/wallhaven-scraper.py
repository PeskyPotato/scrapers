from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from urllib.error import URLError
from time import sleep
import os
import sys


def parsePages(search):
    print("Searching for {}".format(search.replace("%20", " ")))
    page = 1
    while(1):
        print("==== Page {} ====".format(page))
        url = "https://alpha.wallhaven.cc/search?q={}&search_image=&page={}".format(search, page)

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

        figures = page_soup.findAll("figure")

        if len(figures) == 0:
            return

        for figure in figures:
            picture_id = figure["class"][1].split("-")[1]
            saveImage(picture_id)
        sleep(2)
        page += 1
        

def saveImage(picture_id):
    image_url = "https://alpha.wallhaven.cc/wallpaper/{}".format(picture_id)    

    req_one = Request(
        image_url, 
        data=None, 
        headers= {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Connection': 'keep-alive'
        }
    )
    
    uClient = urlopen(req_one)
    image_html = uClient.read()
    uClient.close()
    image_soup = soup(image_html, "lxml")

    author_name = image_soup.findAll("a", {"class":"username"})[0].text
    image_full = image_soup.findAll("img",{"id":"wallpaper"})[0]["src"]
    image_ext = image_full.split(".")[-1]
    print(author_name, "https:" + image_full, image_ext)

    req_two = Request(
        "https:{}".format(image_full), 
        data=None, 
        headers= {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Connection': 'keep-alive'
        }
    )

    try:
        with open("wallpapers/{}-{}.{}".format(author_name, picture_id, image_ext), "wb") as f:
            f.write(urlopen(req_two).read())
    except URLError as e:
        print(e)
        print("Error saving", image_url)


def main():
    if not os.path.exists('wallpapers'):
        os.makedirs('wallpapers')

    search = "pixel"
    if len(sys.argv) > 1:
        search = sys.argv[1].replace(" ", "%20")
    parsePages(search)

if __name__ == "__main__":
    main()