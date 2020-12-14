from bs4 import BeautifulSoup as soup
import requests
import os
import re
import argparse
from multiprocessing.pool import ThreadPool
from tqdm.auto import tqdm

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_URL = "https://downloads.khinsider.com/"


def scrape_album(url):
    print("Starting", url)
    page_html = requests.get(url)
    page_soup = soup(page_html.content, "html5lib")
    album_data = {}
    album_data["name"] = page_soup.find("div", {"id": "EchoTopic"}).find("h2").text
    album_data["date"] = page_soup.find("div", {"id": "EchoTopic"}).find("p", {"align": "left"}).find_all("b")[-1].text

    song_list = []
    song_rows = page_soup.find("table", {"id": "songlist"}).find_all("tr")
    for row in song_rows:
        song_url = row.find("a")
        if not song_url:
            continue
        song_url = BASE_URL + song_url.get("href")
        song_list.extend(scrape_song(song_url, album_data))

    with ThreadPool(processes=4) as tp:
        for imap_result in tp.imap_unordered(download_file, song_list):
            pass

    return

def scrape_song(url, album_data=None):
    print(url)
    page_html = requests.get(url)
    page_soup = soup(page_html.content, "html5lib")

    song_list = []

    urls = page_soup.find("div", {"id": "EchoTopic"}).find_all("a")
    name_original = page_soup.find("div", {"id": "EchoTopic"}).find_all("p", {"align": "left"})[1].find_all("b")[1].text

    for song_url in urls:
        if "Click here to" in song_url.text:
            name = name_original + "." + song_url.get("href", "").split(".")[-1]
            if album_data:
                local_path = os.path.join(BASE_DIR, format_name(album_data.get("name")))
                if not os.path.exists(local_path):
                    os.makedirs(local_path)
                local_file = os.path.join(local_path, format_name(name))
            else:
                local_file = os.path.join(BASE_DIR, format_name(name))

            song_list.append((local_file, song_url.get("href")))
    return song_list


def download_file(data, retries=0):
    local_filename = data[0]
    url = data[1]
    if os.path.isfile(local_filename):
        return url

    try:
        response = requests.get(url, stream=True)
        with tqdm.wrapattr(open(local_filename, "wb"), "write", miniters=1,
                           total=int(response.headers.get('content-length', 0)),
                           desc=local_filename[-20:]) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
    except requests.exceptions.HTTPError:
        if retries > 5:
            return
        print("retrying", url)
        retries += 1
        download_file((local_filename, url), retries)

    return url

def format_name(title):
    title = re.sub('[?/|\\\}{:<>*"]', '', title)
    if len(title) > 190:
        title = title[:120]
    return title

def main():
    parser = argparse.ArgumentParser(description="Downoad albums from Khinsider.")
    parser.add_argument("url", type=str, help="Url to the album page")
    parser.add_argument("-o", "--output", type=str, help="Set download directory")
    args = parser.parse_args()

    global BASE_DIR
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    if args.output:
        BASE_DIR = os.path.abspath(args.output)
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

    url = args.url
    if ".txt" in url:
        with open(url, "r") as f:
            for page_url in f:
                scrape_album(page_url.strip())
    else:
        scrape_album(url)

main()
