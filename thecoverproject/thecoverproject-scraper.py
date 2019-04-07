from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from time import sleep
import os
import re
import json
from multiprocessing import Pool
import sqlite3
import argparse


def scrape(cover_id):
    if dbWrite(cover_id):
        # get cover page
        url = "http://www.thecoverproject.net/view.php?cover_id={}".format(cover_id)

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

        # get cover info
        console = page_soup.findAll("td", {"class":"newsHeader"})[0].a.text.strip()
        cover_info = page_soup.findAll("td", {"class": "pageBody"})
        try:
            info = cover_info[0]
        except IndexError:
            print(cover_id, "not a cover page")
            return

        # parse cover info
        name = info.text.split("Available")[0].strip()
        cover_details = info.text.split("Cover Details:")[1]
        description = re.search('(Description:)(.*)(Format:)', cover_details).group(2).strip()
        format = re.search('(Format:)(.*)(Created by:)', cover_details).group(2).strip()
        created_by = re.search('(Created by:)(.*)(Region:)', cover_details).group(2).strip()
        region  = re.search('(Region:)(.*)(Case Type:)', cover_details).group(2).strip()
        case_type  = re.search('(Case Type:)(.*)(This)', cover_details).group(2).strip()
        img_url = info.findAll("a")[-1]["href"]

        data = {
            "cover_id" : cover_id,
            "name" : name,
            "console" : console,
            "description" : description,
            "format" : format,
            "created_by" : created_by,
            "region" : region,
            "case_type" : case_type,
            "img_url" : img_url
        }

        print(cover_id, name, console)

        # download image and write info to json
        req_two = Request(
            "http://www.thecoverproject.net{}".format(img_url),
            data=None, 
            headers= {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Connection': 'keep-alive'
            }
        )
        direct = "{}/{}/{}/".format(console, name.replace(" ", "_").replace("'","_"), format)

        if not os.path.exists(direct):
            os.makedirs(direct)

        try:
            with open("{}/{}_{}.jpg".format(direct, console, name), "wb") as f:
                f.write(urlopen(req_two).read())
            with open('{}/{}_{}.json'.format(direct, console, name), 'w') as j:  
                json.dump(data, j)

        except URLError as e:
            with open("error.log", "a+") as e:
                e.write("Error saving {} - {}\n".format(img_url, e))
            print(e, img_url)
        
        sleep(1)

    '''
Creates a database file is one does not already
exist.
'''
def createTable():
    conn = sqlite3.connect('cover_ids.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (id TEXT NOT NULL UNIQUE, PRIMARY KEY (id))')
    c.close()
    conn.close()

'''
Enter submission information into the database.
Duplicates return 0 and entry is skippped, otherwise
it is logged and a 0 is returned.
'''
def dbWrite(id):
    try:
        conn = sqlite3.connect('cover_ids.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (id) VALUES (?)", (str(id),))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Duplicate", id, end="\r")
        c.close()
        conn.close()
        return 0

    c.close()
    conn.close()
    return 1


parser = argparse.ArgumentParser()
parser.add_argument("--id", help="Enter a cover_id to download")
args = parser.parse_args()

createTable()

if args.id:
    try:
        scrape(int(args.id))
    except ValueError:
        print("cover_id can only be an integer")
else:
    cover_ids = []
    cover_ids.extend(range(1, 17716))

    agents = 5
    chunksize = 3
    with Pool(processes = agents) as pool:
        pool.map(scrape, cover_ids, chunksize)
