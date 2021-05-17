from bs4 import BeautifulSoup as soup
import requests
import os
import re
import argparse
from multiprocessing.pool import ThreadPool
from tqdm.auto import tqdm
from database import Project, User, Download, Database

import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_URL = "https://smutba.se"


def scrape(project_id):
    db = Database()
    if db.get_project(project_id):
        # print("Project {} exists in the datatbase".format(project_id))
        return True

    url = "https://smutba.se/project/{}/".format(project_id)
    page_html = requests.get(url)
    if page_html.status_code == 404:
        print("Project {} does not exist on the site".format(project_id))
        return False
    page_soup = soup(page_html.content, "html5lib")

    project = Project(project_id)
    project.title = page_soup.find("h1", {"id": "file_title"}).text
    images_e = page_soup.find_all("img", {"class": "project-detail-image-main"})
    for e in images_e:
        project.images.append(e["src"])
    project.description = page_soup.find("div", {"class": "panel__body"}).decode_contents()

    user_id = page_soup.find("h4", {"class": "panel__avatar-title"}).find("a").get("href", "").split("/")[-2]
    user = User(user_id)
    user.name = page_soup.find("span", {"class": "username"}).text
    user.add_user()
    project.user = user

    info = page_soup.find("div", {"class": "panel__footer"}).find_all("dd")
    project.posted = info[0].text
    project.views = info[1].text
    project.category = info[2].text
    project.licence = info[3].text

    trs = page_soup.find("tbody").find_all("tr")
    for i in range(0, len(trs), 2):
        tr = trs[i].find_all("td")
        if len(tr) < 4:
            break
        filename = tr[0].strong.text
        downloads = tr[1].text
        created = tr[2].text
        filesize = tr[3].text
        links = trs[i+1].find_all("a")

        download = Download(filename)
        download.downloads = downloads
        download.created = created
        download.filesize = filesize
        download.project_id = project.id

        for link in links:
            download.urls.append(BASE_URL + link.get("href", ""))
        download.add_download()
    success = project.add_project()
    if not success:
        print("Project {} was not successfully added to the database".format(project_id))
    else:
        print("Project {} added to the database".format(project_id))


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

def download_download_wrapper(data):
    download_file(data[:-1])
    db = Database()
    db.set_download_download(data[2])


def get_file_url(url):
    page_html = requests.get(url)
    if page_html.status_code == 404:
        print("File {} does not exist on the site".format(url))
        return False
    page_soup = soup(page_html.content, "html5lib")
    file_url = page_soup.find("div", {"class": "project-description-div"}).find("a").get("href", "")
    return file_url


def format_name(title):
    title = re.sub('[?/|\\\}{:<>*"]', '', title)
    if len(title) > 190:
        title = title[:120]
    return title


def download_all():
    db = Database()
    download_list = db.get_not_downloaded_download()
    download_list_urls = []
    for download in download_list:
        urls = db.get_url(download[0])
        if not urls:
            print(f"No URL for Project {download[0]}")
            continue
        url = get_file_url(urls[0][1])
        if not url:
            continue
        file_dir = os.path.join(BASE_DIR, "project", str(download[5]).zfill(5))
        file_location = os.path.join(file_dir, format_name(download[1]))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        download_list_urls.append((file_location, url, download[0]))

    with ThreadPool(processes=4) as tp:
        for imap_result in tp.imap_unordered(download_download_wrapper, download_list_urls):
            pass

    project_list = db.get_not_downloaded_project()
    for project in project_list:
        images = db.get_image_urls(project[0])
        for image in images:
            file_dir = os.path.join(BASE_DIR, "project", str(project[0]).zfill(5), "images")
            file_location = os.path.join(file_dir, os.path.basename(image[1]))
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            download_file((file_location, image[1]))
            db.set_download_project(project[0])


def main():
    parser = argparse.ArgumentParser(description="Archive assets from Smutbase and Open3DLab")
    parser.add_argument("--start", type=int, help="Starting project ID", default=1)
    parser.add_argument("--end", type=int, help="Ending project ID", default=32500)
    parser.add_argument("-o", "--output", type=str, help="Set download directory")
    args = parser.parse_args()

    global BASE_DIR
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    if args.output:
        BASE_DIR = os.path.abspath(args.output)
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

    for project_id in range(args.start, args.end+1):
        scrape(project_id)

    download_all()


main()
