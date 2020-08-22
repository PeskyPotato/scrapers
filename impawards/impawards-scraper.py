from bs4 import BeautifulSoup as soup
import requests
import re
from multiprocessing.pool import ThreadPool
import os
import argparse

HEADERS = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
}
BASE_URL = "http://www.impawards.com"
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def scrape(page):
    print("Page", page)
    url = BASE_URL + "/alpha{}.html".format(page)
    page_html = requests.get(url, headers=HEADERS).content
    page_soup = soup(page_html, "html5lib")

    posters = page_soup.findAll("div", {"class": "constant_thumb"})
    posters_dl = []
    for poster in posters:
        src = poster.center.a.img["src"].replace("med_", "")
        src_xlg = src.replace(".jpg", "_xlg.jpg")
        src_xxlg = src.replace(".jpg", "_xxlg.jpg")
        year = re.search(r"\(([\d]+)\)$", poster.div.text).group(1)
        file_dir = os.path.join(BASE_DIR, "posters", year)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        posters_dl.append((os.path.join(file_dir, src.split("/")[-1]), BASE_URL + src))
        posters_dl.append((os.path.join(file_dir, src_xlg.split("/")[-1]), BASE_URL + src_xlg))
        posters_dl.append((os.path.join(file_dir, src_xxlg.split("/")[-1]), BASE_URL + src_xxlg))

    if not posters_dl:
        return False

    with ThreadPool(processes=8) as tp:
        for imap_result in tp.imap_unordered(download_file, posters_dl):
            pass
    return True


def download_file(data):
    local_filename = data[0]
    url = data[1]
    if os.path.isfile(local_filename):
        print("{:15}{}".format("Skipped", local_filename.split("/")[-1]))
        return local_filename

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.exceptions.HTTPError:
        print("{:15}{}".format("Not found", local_filename.split("/")[-1]))
        return False

    print("{:15}{}".format("Downloaded", local_filename.split("/")[-1]))
    return local_filename


def main():
    parser = argparse.ArgumentParser(description="Archive posters from impawards.com")
    parser.add_argument("--start", type=int, help="Starting pages number", default=1)
    parser.add_argument("--end", type=int, help="Ending page number", default=-1)
    parser.add_argument("-o", "--output", type=str, help="Set download directory")
    args = parser.parse_args()

    global BASE_DIR
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    if args.output:
        BASE_DIR = os.path.abspath(args.output)
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

    page = args.start
    page_end = args.end
    stop = True
    while(stop):
        try:
            stop = scrape(page)
        except requests.exceptions.ConnectionError:
            stop = scrape(page)
        page += 1
        if page_end != -1 and page > page_end:
            stop = False


if __name__ == "__main__":
    main()
