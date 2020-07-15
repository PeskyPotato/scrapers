import http.cookiejar
import requests
import os
import re
from bs4 import BeautifulSoup as soup
import json
from multiprocessing.pool import ThreadPool
import argparse

cj = http.cookiejar.MozillaCookieJar('cookies.txt')
cj.load()

BASE = "https://www.wad-archive.com"
PROCESSES = 8


def download_file(in_args):
    eg_file = in_args[0]
    eg_link = in_args[1]

    if eg_link == "?df=1":
        print("No download for", eg_file)
        return

    if not os.path.isfile(eg_file):
        print("Downloading", eg_link)
        response = requests.get(eg_link, cookies=cj, stream=True)
        with open(eg_file+".part", "wb") as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
        try:
            os.rename(eg_file + ".part", eg_file)
        except FileNotFoundError:
            print("Skipping", eg_file)
    else:
        print("Skippping duplicate", eg_link, end="\r")


def format_name(title):
    title = re.sub('[?/|\\\}{:<>*"]', '', title)
    if len(title) > 190:
        title = title[:120]
    return title


def wad_info(url):
    data = {}
    page_html = requests.get(url, cookies=cj).content
    page_soup = soup(page_html, "lxml")

    name = page_soup.find("h1", {"class": "break-all"})
    data["name"] = name.text.strip()

    data_type = page_soup.find("div", {"class": "panel-body"}).find_all("div", {"class": "col-md-3 col-xs-12"})
    data_value = page_soup.find("div", {"class": "panel-body"}).find_all("div", {"class": "col-md-9 col-xs-10 col-xs-offset-2 col-md-offset-0"})

    for i in range(0, len(data_value)):
        data[data_type[i].text.strip()] = data_value[i].text.strip()

    side_panel = page_soup.find("div", {"class": "col-lg-4 col-md-4 col-xs-12 col-xs-12-float-right main-image"})
    description = side_panel.find("p").text
    image = side_panel.a["href"]

    data["image"] = image
    data["description"] = description

    readme = []

    readme_e = page_soup.find_all("pre", {"class": "readme"})
    for e in readme_e:
        readme.append(e.text)
    data["readme"] = readme

    data["download"] = ""
    download = page_soup.find("ul", {"class": "wad-links"}).find("a")
    if download:
        download = download["href"]
        data["download"] = BASE + download

    discs = []
    discs_e = page_soup.find("div", {"class": "ibox"}).find_all("a")
    for e in discs_e:
        discs.append({"name": e["title"], "url": BASE + e["href"]})
    data["discs"] = discs

    file_dir = os.path.join("wad", format_name(data["name"]+"_"+data["MD5"]))
    file_location = os.path.join(file_dir, format_name(os.path.basename(data["download"])))
    if not os.path.exists(file_dir):
        try:
            os.makedirs(file_dir)
        except FileExistsError:
            print("FileExistsError", file_location)
            pass

    with open(os.path.join(file_dir, "{}_{}.json".format(format_name(data["name"]), data["MD5"])), "w+") as f:
        json.dump(data, f)

    download_file((file_location, data["download"] + "?df=1"))
    return (file_location, data["download"] + "?df=1")


def disc_info(url):
    print("==== DISC:", url, "====")
    data = {}

    page_html = requests.get(url, cookies=cj).content
    page_soup = soup(page_html, "lxml")

    name = page_soup.find("h1", {"class": "break-all"})
    data["name"] = name.text.strip()
    description = page_soup.find("div", {"class": "panel-description"})
    data["description"] = description.text.strip()

    data_type = page_soup.find_all("div", {"class": "col-xs-3"})
    data_value = page_soup.find_all("div", {"class": "col-xs-9"})

    for i in range(0, len(data_value)):
        data[data_type[i].text.strip()] = data_value[i].text.strip()

    wad_list = []
    download_queue = []
    r_disc = re.compile('.*disc-.*')
    wad_list_e = page_soup.find_all("ul", {"id": r_disc})
    for wad_group in wad_list_e:
        for wad in wad_group.find_all("a"):
            wad_list.append({"name": wad.text, "url": BASE + wad["href"]})
            download_queue.append(BASE + wad["href"])

    data["wad_list"] = wad_list

    file_dir = os.path.join("disc")
    file_location = os.path.join(file_dir, format_name(data["name"]) + ".json")
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    with open(file_location, "w+") as f:
        json.dump(data, f)
    print(PROCESSES)
    with ThreadPool(processes=PROCESSES) as tp:
        for imap_result in tp.imap_unordered(wad_info, download_queue):
            pass

    return data


def get_discs():
    for page in range(0, 70, 10):
        url = "https://www.wad-archive.com/category/Discs/{}".format(page)
        page_html = requests.get(url, cookies=cj).content
        page_soup = soup(page_html, "lxml")

        discs_e = page_soup.find_all("div", {"class": "result-element"})
        for e in discs_e:
            disc_info(BASE + e.find("a")["href"])


def main():
    parser = argparse.ArgumentParser(description="Archive documents from riksdagen.se")
    parser.add_argument("-p", "--processes", type=int, help="Set number of concurrent downloads")
    args = parser.parse_args()

    global PROCESSES
    if args.processes:
        PROCESSES = args.processes

    get_discs()


main()
