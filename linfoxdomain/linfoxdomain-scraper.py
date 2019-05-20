from time import sleep
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup as soup
import os

def scrape(category, down_path):
    if not os.path.exists(down_path):
        os.makedirs(down_path)

    base_url = "http://linfoxdomain.com"
    if (category == "flash"):
        get_flash_links(base_url, down_path)

def get_flash_links(base_url, down_path):
    links = []
    req = Request(
        base_url + "/flash", 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    uClient = urlopen(req)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "lxml")

    # first part of flash games
    links = page_soup.find_all("td", {"class":"th"})
    for link in links:
        req = Request(
            base_url + link.a["href"], 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        uClient = urlopen(req)
        game_html = uClient.read()
        uClient.close()
        game_soup = soup(game_html, "lxml")
        print(link.a["href"])
        try:
            download_link = game_soup.find_all("object")[0]["data"]
        except KeyError:
            try:
                download_link = game_soup.find_all("embed")[0]["src"]
            except IndexError:
                print("no download link found")
                continue

        file_path = down_path + "/" + download_link.split("/")[-1]
        download(file_path, base_url, download_link)
        sleep(1)
    
    # second part of flash games, table at the bottom of the page
    columns = page_soup.find_all("td", {"class":"nobr"})
    for column in columns:
        for link in column.find_all("a"):
            req = Request(
                base_url + link["href"], 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            uClient = urlopen(req)
            game_html = uClient.read()
            uClient.close()
            game_soup = soup(game_html, "lxml")
            print(link["href"])
            try:
                download_link = game_soup.find_all("object")[0]["data"]
            except KeyError:
                try:
                    download_link = game_soup.find_all("embed")[0]["src"]
                except IndexError:
                    print("no download link found")
                    continue

            file_path = down_path + "/" + download_link.split("/")[-1]
            download(file_path, base_url, download_link)
            sleep(1)

def download(file_path, base_url, download_link):
    if not os.path.isfile(file_path):
        try:
            r = requests.get(base_url + str(download_link), stream = True)
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except KeyboardInterrupt:
            os.remove(file_path)
            exit()
    else:
        print("skip")

def main():
    scrape("flash", "flash_games")
 
main()