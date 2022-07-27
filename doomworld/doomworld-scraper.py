from bs4 import BeautifulSoup as soup
import requests
import os
import re
import argparse
from tqdm.auto import tqdm
from database import File, Author, Database


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_URL = ""


def scrape():
    db = Database()
    db.create_tables()

    # TODO: parse all categories
    categories = [
        "2-combos", "3-deathmatch", "4-deathtag", "5-doombot", "6-skulltag",
        "7-docs", "8-editing", "9-gaqs", "10-misc", "11-multiplayer",
        "12-graphics", "13-historic", "14-idstuff", "15-doom", "17-doom2",
        "18-doom3", "19-source", "24-heretic", "25-hexen", "54-source",
        "62-wolf3d", "63-levels", "64-doom"
    ]
    for category in categories:
        page_exists = True
        page = 1
        while page_exists:
            url = f"https://www.doomworld.com/files/category/{category}/?page={page}/"

            page_html = requests.get(url)
            if page_html.status_code == 404:
                print(f"{category}: Page {page} does not exist on the site")
                page_exists = False
            elif page_html.status_code == 303:
                print(f"{category}: End of category")
                page_exists = False
                break

            page_soup = soup(page_html.content, "html5lib")
            files = page_soup.find(
                "ol", {"class": "ipsDataList ipsClear ipsDataList_large"}
            )
            if not files:
                print(f"{category}: No files in category")
                break

            files = files.find_all("li", {"class": "ipsDataItem"})

            for file_e in files:
                file_url = file_e.find("a").get("href")
                file_title = file_e.find_all("a")[1].text
                file_id = get_id(file_url)

                author_e = file_e.find(
                    "p", {"class": "ipsType_reset ipsType_light ipsType_blendLinks"}
                )
                author_a = author_e.find("a")
                author_id = 0
                if author_a:
                    author_id = get_id(author_a.get("href"))
                author_name = author_e.text.strip()
                author_name = re.search(r"\b(\w+)$", author_name).group(1)

                author = Author(author_id)
                author.name = author_name
                author.add_author()

                # Get file details
                file = File(file_id)
                file.author = author
                file.title = file_title

                if file.check_download():
                    print(f"{category}: {page} {file.title} downloaded")
                    continue

                session = requests.Session()
                file_html = session.get(file_url)
                if file_html.status_code == 404:
                    print(f"File {file.id} does not exist on the site")
                    return False
                file_soup = soup(file_html.content, "html5lib")
                file.description = file_soup.find(
                    "div",
                    {"class": "ipsType_richText ipsContained ipsType_break"}
                ).text.strip()
                file.download_url = file_soup.find(
                    "a",
                    {"class": "ipsButton ipsButton_fullWidth ipsButton_large ipsButton_important"}
                ).get("href")
                # TODO: get all metadata from file page

                print(f"{category}: {page} - {file.title}")
                file.add_file()

                file_dir = os.path.join(BASE_DIR, "file", category, file_id)
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)

                # TODO: download all images from file page

                # TODO: skip file is marked as downloaded
                try:
                    response = download_file(
                        [file_dir, file.download_url], session
                    )
                except Exception as e:
                    print(f"{category}: {page} {file.title} failed to download, {e}")
                    response = False
                if response:
                    db.set_download(file_id)
            page += 1


def get_id(url):
    return re.search(r"((\d)+-(.)+)/", url).group(1)


def download_file(data, session, retries=0):
    local_filename = data[0]
    url = data[1]
    try:
        response = session.get(url, stream=True)
        local_filename = os.path.join(
            local_filename, os.path.basename(response.url)
        )
        if os.path.isfile(local_filename):
            print("File exists")
            return False

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
        download_file((local_filename, url), session, retries)
    return url


def main():
    parser = argparse.ArgumentParser(description="Archive files from DoomWorld")
    parser.add_argument("-o", "--output", type=str, help="Set download directory")
    args = parser.parse_args()

    global BASE_DIR
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    if args.output:
        BASE_DIR = os.path.abspath(args.output)
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

    scrape()


main()
