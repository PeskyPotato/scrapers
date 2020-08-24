import time
from bs4 import BeautifulSoup as soup
from multiprocessing import Pool
import requests
import json
import re
import sys
import os

def grab_papers(url, volume=1, issue=1):
    base_directory = os.getcwd()
    pdfs = []

    print("Volume", volume, "Issue", issue)
    folders = os.path.join(base_directory, "volume_{}".format(volume),
                            "issue_{}".format(issue))
    if not os.path.exists(folders):
        os.makedirs(folders)

    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }
    page_html = requests.get(url, headers = headers).content

    page_soup = soup(page_html, "html5lib")
    table = page_soup.find("table")

    for row in table.findAll("tr"):
        data = {}
        t_data = row.findAll("td")
        data["title"] = t_data[0].p.text
        data["authors"] = t_data[0].findAll("p")[1].text
        data["pdf_url"] = "http://www.ijssb.com{}".format(t_data[1].find("a")["href"])

        with open(os.path.join(folders, format_name(data["title"]) + ".json"), "w") as f:
            json.dump(data, f)

        pdfs.append((data, folders))

    pool = Pool(processes=4)
    pool.map(download, pdfs)
    pool.close()
    pool.join()

def format_name(title):
    title = re.sub('[?/|\\\}{:<>*"]', '', title)
    if len(title) > 110:
        title = title[:110]
    return title

def download(param):
    print(param[0]["pdf_url"])
    r = requests.get(param[0]["pdf_url"], stream = True)
    with open(os.path.join(param[1], format_name(param[0]["title"]) + ".pdf"), "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

grab_papers("http://www.ijssb.com/index.php/archive/9-contact/11-vol-1no-1", 1, 1)
grab_papers("http://www.ijssb.com/index.php/archive/9-contact/9-vol-12", 1, 2)
grab_papers("http://www.ijssb.com/index.php/archive/9-contact/8-vol-1-no-3-november-2016", 1, 3)
grab_papers("http://www.ijssb.com/index.php/archive/9-contact/6-vol-1-no-4-december-2016", 1, 4)
grab_papers("http://www.ijssb.com/index.php/archive/9-contact/5-vol-2-no-1-february-2017", 2, 1)
grab_papers("http://www.ijssb.com/index.php/archive/9-contact/4-vol-2-no-2-april-2017", 2, 2)
grab_papers("http://www.ijssb.com/index.php/archive/9-contact/3-vol-2-no-3-june-2017", 2, 3)
grab_papers("http://www.ijssb.com/index.php/archive/9-contact/2-vol-2-no-4-august-2017", 2, 4)
grab_papers("http://www.ijssb.com/index.php/archive/2-uncategorised/35-vol-2-no-5-november-2017", 2, 5)
grab_papers("http://www.ijssb.com/index.php/archive/2-uncategorised/36-vol-3-no-1-march-2018", 3, 1)
grab_papers("http://www.ijssb.com/index.php/archive?id=37", 3, 2)
grab_papers("http://www.ijssb.com/index.php/archive/2-uncategorised/38-vol-3-no-3-november-2018", 3, 3)
grab_papers("http://www.ijssb.com/index.php/archive/2-uncategorised/39-vol-4-no-1-march-2019", 4, 1)
grab_papers("http://www.ijssb.com/index.php/archive/2-uncategorised/42-vol-4-no-2-june-2021", 4, 2)
grab_papers("http://www.ijssb.com/index.php/current", 4, 3)
