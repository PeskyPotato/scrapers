from bs4 import BeautifulSoup as soup
import shutil
import requests
from multiprocessing.pool import ThreadPool
import time
import os
import argparse

download_direct = os.path.join(os.path.dirname(__file__), 'images')

def scrape(end=1, start=1, term=""):
    print("============={} of {}=============".format(start, end))
    if (term != ""):
        url = "https://www.wallpaperflare.com/search?wallpaper={}&page={}".format(term, start)
    else:
        url = "https://www.wallpaperflare.com/index.php?c=main&m=portal_loadmore&page={}".format(start)
    
    page_soup = soup(requests.get(url).content, "html5lib")

    imgs = page_soup.findAll("li", {"itemprop":"associatedMedia"})
    img_urls = []
    for img in imgs:
        img_page = img.find("a", {"itemprop":"url"})["href"] + "/download/"
        img_urls.append(get_url(img_page))

    with ThreadPool(processes=10) as tp:
        map_start = time.time()
        for imap_result in tp.imap_unordered(download_file, img_urls):
            print("{} - {:.2f} seconds".format(imap_result, time.time() - map_start))

    if (start < end):
        start += 1
        scrape(start=start, end=end, term=term)


def get_url(img_page):
    page_soup = soup(requests.get(img_page).content, "html.parser")
    return page_soup.find("img", {"id":"show_img"})["src"]

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(os.path.join(download_direct, local_filename), "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename


if __name__ == "__main__":
        
    if not os.path.exists(download_direct):
        os.makedirs(download_direct)

    parser = argparse.ArgumentParser(description="Scrape wallpapers from WallpaperFlare.")
    parser.add_argument("--start", type=int, help="Starting page")
    parser.add_argument("--end", type=int, help="Ending page")
    parser.add_argument("--search_term", type=str, help="Search term")
    parser.set_defaults(start=1, search_term="", end=52)

    args = parser.parse_args()
    scrape(start=args.start, end=args.end, term=args.search_term)
