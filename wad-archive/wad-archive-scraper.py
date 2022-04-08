from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup as soup
import requests
import argparse
import os
import logging
from tqdm.auto import tqdm
import re

from database import WAD, Database

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def format_name(name):
    name = re.sub('[?/|\\\}{:<>*"]', '', name)
    if len(name) > 190:
        name = name[:120]
    return name


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
        logging.info("retrying", url)
        retries += 1
        download_file((local_filename, url), retries)

    return url


def download_download_wrapper(data):
    download_file(data[:-1])
    db = Database()
    db.set_wad_downloaded(data[2])


def download_all():
    # get all undownloaded WADs
    db = Database()
    download_list = db.get_not_downloaded_wads()
    download_list_urls = []
    for download in download_list:
        wad = WAD(download[0])
        urls = db.get_wad_url(wad)
        if urls:
            url = urls[0][1]
            file_dir = os.path.join(BASE_DIR, wad.id)
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            filename = os.path.join(
                file_dir,
                format_name(f"{wad.id}-{os.path.basename(url)}")
            )
            download_list_urls.append((filename, url, wad))

    # download WADS
    with ThreadPool(processes=4) as tp:
        for imap_result in tp.imap_unordered(
            download_download_wrapper,
            download_list_urls
        ):
            pass
    # mark downlaoded in database if successful
    pass


def get_items():
    wads = []
    # wad_types = ["PWAD", "PK3", "IWAD", "PK7", "WAD2", "WAD3", "PKE", "ZWAD"]
    wad_types = ["PWAD", "PK3", "IWAD", "PK7", "WAD2", "WAD3", "PKE", "ZWAD"]
    for wad_type in wad_types[3:]:
        wads = wads + get_items_by_type(wad_type)
        logging.info(f"Currently {len(wads)} fetched.")
    return wads


def get_items_by_type(wad_type):
    page = 1
    wads = []
    while True:
        logging.info(f"Fetching {wad_type} WADs, page {page}")
        page += 1
        logging.debug(f"WAD_TYPE {wad_type}, page {page}")
        url = f"https://www.wad-archive.com/Category/WADs/Wad-Type/{wad_type}/{page}"

        page_response = requests.get(url, allow_redirects=False)
        if not page_response.ok:
            logging.error(f"Page {page} of type {wad_type} has an issue.")
            continue
        if (page_response.status_code > 300 and page_response.status_code < 399) or (page_response == 404):
            logging.debug(f"end of {wad_type}")
            break

        page_soup = soup(page_response.content, "html5lib")

        wads_div = page_soup.find("div", {"class": "d-flex flex-wrap"})
        wads_element = wads_div.find_all(
            "div", {"class": "d-flex flex-column flex-grow-1 pl-3 w-66"}
        )

        db = Database()
        for wad in wads_element:
            wad_link = wad.find("a").get("href")
            wads.append("https://www.wad-archive.com/" + wad_link)
            wad = WAD(wad_link.split("/")[-1])
            db.insert_wad(wad)
            get_item_metadata(wad_link.split("/")[-1])

    return wads


def get_item_metadata(wad_id):
    # check if wad_id exists in database
    logging.debug(f"Fetching metadata for {wad_id}")
    db = Database()
    wad_db = db.get_wad(wad_id)

    # fetch page with wad_id
    url = f"https://www.wad-archive.com/wad/{wad_id}"
    page_resp = requests.get(url)
    if not page_resp.ok:
        logging.error(f"WAD {wad_id} has an issue.")

    page_soup = soup(page_resp.content, "html5lib")

    # collect WAD metadata and enter in database
    wad = WAD(wad_id)
    metadata_table = page_soup.find("div", {"class": "col-lg-8 order-lg-2"})
    for item in metadata_table.findAll("div"):
        item_content = item.findAll("div")
        if len(item_content) == 2:
            item_key = item_content[0].text
            item_value = item_content[1].text
            if item_key == "Filenames":
                wad.filenames = item_value
            elif item_key == "Size":
                wad.size = item_value
            elif item_key == "MD5":
                wad.md5 = item_value
            elif item_key == "SHA-1":
                wad.sha1 = item_value
            elif item_key == "SHA-256":
                wad.sha256 = item_value
            elif item_key == "WAD Type":
                wad.wad_type = item_value
            elif item_key == "IWAD":
                wad.iwad = item_value
            elif item_key == "Engines":
                wad.engines = item_value
            elif item_key == "Lumps":
                wad.lumps = item_value
            else:
                logging.debug(f"WAD metadata key {item_key} is unknown.")

    if wad_db:
        db.replace_wad(wad)
    else:
        db.insert_wad(wad)

    link_e = page_soup.find("ul", {"class": "downloadlinks"})
    links = [a.get("href") for a in link_e.find_all("a")]
    for link in links:
        if link.startswith("/wad/"):
            link = "https://www.wad-archive.com" + link
        db.insert_download_url(wad, link)


def main():
    parser = argparse.ArgumentParser(description="Archive assets from wad-archive.com")
    parser.add_argument("-o", "--output", type=str, help="Set download directory")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    global BASE_DIR
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    arg_level = logging.INFO
    if args.verbose:
        arg_level = logging.DEBUG

    logging.basicConfig(
        level=arg_level,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M'
    )

    if args.output:
        BASE_DIR = os.path.abspath(args.output)
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

    logging.info("Fetching WADs")
    get_items()

    logging.info("Downloading WADS")
    download_all()


main()
