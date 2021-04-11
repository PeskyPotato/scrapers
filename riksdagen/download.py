import requests
import os
from tqdm.auto import tqdm
from multiprocessing.pool import ThreadPool
from database import Database
import re


def download_file(local_filename, url):
    print("Downloading", local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def download(in_args):
    eg_file = in_args[0]
    eg_link = in_args[1]
    try:
        response = requests.get(eg_link, stream=True)
    except Exception as e:
        print(e)
        return False
    try:
        with tqdm.wrapattr(open(eg_file, "wb"), "write", miniters=1,
                           total=int(response.headers.get('content-length', 0)),
                           desc=eg_file[-20:]) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
    except requests.exceptions.ChunkedEncodingError as e:
        print(e)
        return False
    db = Database()
    db.set_download(in_args[2])
    db.__del__()


def format_name(title):
    title = re.sub('[?/|\\\}{:<>*"]', '', title)
    if len(title) > 190:
        title = title[:120]
    return title


def download_main(download_dir):
    print("Downloading to", download_dir)

    db = Database()
    debates = db.get_download()
    db.__del__()

    img_urls = []
    for debate in debates:
        if debate[3] and debate[4] == 0:
            title = debate[1]
            if title == "" or title is None:
                title = "no_title"
            date = debate[2]
            if date == "" or date is None:
                date = "no_date"

            name = os.path.join(download_dir, format_name(date))
            if not os.path.exists(name):
                os.makedirs(name)
            name = os.path.join(name, format_name("{}-{}.mp4".format(str(debate[0]), str(title))))
            img_urls.append((name, debate[3], debate[0]))

    with ThreadPool(processes=4) as tp:
        for imap_result in tp.imap_unordered(download, img_urls):
            pass
