from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from urllib.error import HTTPError
from time import sleep
import os
import sys

def scrape_page():

    page = 8
    while(1):
        print("==== Page", page, " ====")
        url = "https://iconmonstr.com/page/{}".format(page)

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

        icons = page_soup.findAll("div", {"class": "content-items-thumb-wrap"})
        for icon in icons:
            icon_url = icon.a["href"]
            scrape_icon(icon_url)
    
        page += 1

def scrape_icon(url):
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

    name  = url.split("/")[-2][:-4]

    for form in page_soup.findAll("div", {"class": "toggle-btn"}):
        url = "https://iconmonstr.com/{}-{}/".format(name, form["id"])
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
        print(url)
        if form["id"] == "png":
            n = page_soup.findAll("h3", {"class": "date"})[0]["id"]
            i = page_soup.findAll("div", {"class": "active toggle-btn"})[0]["id"]
            r = name
            o = form["id"]
            download_url = "https://iconmonstr.com/wp-content/g/gd/png.php?size=240&padding=0&icon=assets/source/{}/png/iconmonstr-{}.png&in=iconmonstr-{}.png&bgShape=&bgColorR=200&bgColorG=200&bgColorB=200&iconColorR=0&iconColorG=0&iconColorB=0".format(n, name, name)
        elif form["id"] != "font":
            t = page_soup.findAll("h3", {"class": "active-id"})[0]["id"][:32]
            n = page_soup.findAll("h3", {"class": "date"})[0]["id"]
            i = page_soup.findAll("div", {"class": "active toggle-btn"})[0]["id"]
            r = page_soup.findAll("div", {"class": "download-btn"})[0]["id"]
            o = page_soup.findAll("div", {"class": "container-content-preview"})[0]["id"]
            download_url = "https://iconmonstr.com/?s2member_file_download_key=" + t + "&s2member_file_download=" + n + "/" + i + "/iconmonstr-" + r + "." + o

        path = "./icons/" + r + "/"
        if not os.path.isdir(path):
            os.makedirs(path)
        if not os.path.exists(path + r + "." + o):
            try:
                urlretrieve(download_url, path + r + "." + o)
                print(download_url)
            except HTTPError as e:
                print(download_url)
                with open("error.log", "a+") as error:
                    error.write(download_url + "\n")
        else:
            print("skip", r, end="\r")


scrape_page()