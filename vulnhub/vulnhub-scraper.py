#!/usr/bin/env python3

from bs4 import BeautifulSoup as soup
from urllib.request import Request
from urllib.request import urlopen
from time import sleep
import os
import re
import json
import sys

def scrape(first, last):
    item_data = []
    for page in range(first, last):
        print("==== Page", page, " ====")
        url = "https://www.vulnhub.com/?page={}".format(page)

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

        items = page_soup.findAll("div", {"class": "span12 entry"})
        for item in items:
            title = item.find_all("h1")[0].text
            description = item.find_all("div", {"class": "right"})[0].text.strip()

            sha = item.find_all("div", {"class": "span4 content-footer-1"})[0].text.strip()
            sha = re.sub(r'^(SHA1: )', '', sha)

            links = []
            walkthroughs = []
            link_items = item.find_all("div", {"class": "modal-body"})
            if len(link_items) == 2:
                for link in link_items[0].find_all("li"):
                    point = {}
                    point["text"] = link.a.text
                    point["link"] = link.a["href"]
                    walkthroughs.append(point)
                for link in link_items[1].find_all("li"):
                    for a_s in link.find_all("a"):    
                        links.append(a_s["href"])    
            else:
                try:                
                    for link in link_items[0].find_all("li"):
                        for a_s in link.find_all("a"):    
                            links.append(a_s["href"])                 
                except AttributeError:
                    pass

            data = {}
            data["title"] = title
            data["description"] = description
            data["sha1"] = sha
            data["download"] = links
            data["walkthroughs"] = walkthroughs

            item_data.append(data)
            print(title)

        sleep(1)

    with open("items.json", "w+") as f:
        json.dump(item_data, f)
    print(len(item_data))


def main():
    if len(sys.argv) != 3:
        sys.exit(f"Specify <first page> <last page>")
    try:
        first = int(sys.argv[1])
        last = int(sys.argv[2])
    except ValueError:
        sys.exit("Only use integers")

    scrape(first, last + 1)

main()