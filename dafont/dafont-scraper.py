from time import sleep
from random import randint
from re import sub
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup as soup
import os
from multiprocessing import Pool

def grab_fonts(category, x = "theme"):
    direct = os.getcwd()

    page = 1
    old_name = ""
    new_name = ""

    while(1):
        print("Category: ", category, "Page: ", page)

        url = 'https://www.dafont.com/{}.php?cat={}&page={}'.format(x, category, page)
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

        cat = page_soup.find_all("div", {"class":"dffont2"})
        cat = cat[0].text.replace(">", "-")
        download_direct = direct + "/" + "/" + cat + "/"

        if not os.path.exists(download_direct):
            os.makedirs(download_direct)
        
        authors = page_soup.find_all("div", {"class": "lv1left dfbg"})
        #print(authors[0].find_all("a")[1].text)

        fonts = page_soup.find_all("a", {"class": "dl"})
        old_name = new_name
        new_name = fonts[0]["href"].split("=")[1]

        if (old_name != new_name):
            for (font, author) in zip(fonts, authors):
                link = "https:" + font["href"]
                try:
                    name = link.split("=")[1] + "_by_" + author.find_all("a")[1].text + ".zip"
                    name = name.replace("/", "")
                except IndexError:
                    name = link.split("=")[1] + ".zip"
                    name = name.replace("/","")

                r_zip = requests.get(link, stream=True, headers={"User-agent": "Mozilla/5.0"})
                if not os.path.exists(download_direct + name):
                    print("Downloading ", name, "in", cat)
                    with open(download_direct + name, "wb") as f:
                        f.write(r_zip.content)
        else:
            print("complete")
            break
        
        page +=1 



categories = []
categories.extend(range(101, 119))
categories.extend(range(201, 207))
categories.extend(range(301, 305))
categories.extend(range(501, 505))
categories.extend(range(601, 609))
categories.extend(range(701, 722))
categories.extend(range(801, 806))

agents = 5
chunksize = 3
with Pool(processes = agents) as pool:
    pool.map(grab_fonts, categories, chunksize)

grab_fonts(0, "bitmap")

