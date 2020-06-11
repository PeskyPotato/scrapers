import requests
import os
from tqdm.auto import tqdm
import time
from multiprocessing.pool import ThreadPool
from database import Database


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
    response = requests.get(eg_link, stream=True)
    with tqdm.wrapattr(open(eg_file, "wb"), "write", miniters=1,
                       total=int(response.headers.get('content-length', 0)),
                       desc=eg_file[-20:]) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)


def main():
    download_dir = os.path.dirname(os.path.realpath(__file__))
    print("Downloading to", download_dir)

    db = Database()
    debates = db.get_download()

    img_urls = []
    for debate in debates:
        if all(debate):
            name = os.path.join(download_dir, debate[2])
            if not os.path.exists(name):
                os.makedirs(name)
            name = os.path.join(name, "{}-{}.mp4".format(str(debate[0]), str(debate[1])))
            img_urls.append((name, debate[3]))

    with ThreadPool(processes=2) as tp:
        map_start = time.time()
        for imap_result in tp.imap_unordered(download, img_urls):
            print("{} - {:.2f} seconds".format(imap_result, time.time() - map_start))


main()
