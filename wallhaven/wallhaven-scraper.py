from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from time import sleep
import os
import argparse
# from dataclasses import dataclass

# TODO
# @dataclass
# class parameters:
#     query: str
#     y: float
#     z: float = 0.0


def parsePages(query, categories, purity, sorting, order, colors):
    print("Searching for {}".format(query.replace("%20", " ")))
    page = 1
    while(1):
        print("==== Page {} ====".format(page))
        url = "https://wallhaven.cc/search?q={}&categories={}&purity={}&sorting={}&order={}&page={}".format(query, categories, purity, sorting, order, page)
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
    image_url = "https://wallhaven.cc/w/{}".format(picture_id)

    req_one = Request(
        image_url,
        data=None,
        headers={
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
    author_name = image_soup.findAll("a", {"class": "username"})
    if not author_name:
        author_name = "deleted"
    else:
        author_name = author_name[0].text
    image_full = image_soup.findAll("img", {"id": "wallpaper"})[0]["src"]
    image_ext = image_full.split(".")[-1]
    print(author_name, "https:" + image_full)

    req_two = Request(
        image_full,
        data=None,
        headers={
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
    q = ""
    categories = "111"
    purity = "100"
    sort = "relevance"
    order = "desc"
    colors = ""
    parser = argparse.ArgumentParser()
    parser.add_argument("--sort", help="suported keywords relevance, random, date_added, views, favorites, toplist", default="relevance")
    parser.add_argument("query", help="enter serach term")
    args = parser.parse_args()

    if args.sort in ["relevance", "random", "date_added", "views", "favorites", "toplist"]:
        sort = args.sort

    if args.query:
        q = args.query.replace(" ", "%20")

    if not os.path.exists('wallpapers'):
        os.makedirs('wallpapers')

    parsePages(q, categories, purity, sort, order, colors)


if __name__ == "__main__":
    main()
