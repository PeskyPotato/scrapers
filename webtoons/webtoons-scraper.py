from bs4 import BeautifulSoup as soup
from multiprocessing.pool import ThreadPool
import argparse
import requests
import time
import os
import re

valid_url = r"https?://www.webtoons.com/(?P<language>[a-zA-Z]+)/(?P<genre>[a-zA-Z\-]+)/(?P<title_string>[a-zA-Z0-9_-]*)/(?P<episode_string>[a-zA-Z0-9_-]+)/viewer\?title_no=(?P<title_no>[0-9]+)&episode_no=(?P<episode_no>[0-9]+)"


def parse(url):
    r = requests.get(url, cookies={'ageGatePass': 'true'})

    if (r.status_code != requests.codes.ok):
        print(f"HTTP status code: {r.status_code}")
        return r.status_code

    m = re.match(valid_url, r.url)
    title = m.group('title_string')
    episode = m.group('episode_string')
    episode_no = m.group('episode_no')
    print(episode)

    directory = os.path.join(title, f"{episode_no}-{episode}")
    if not os.path.exists(directory):
        os.makedirs(directory)

    page_soup = soup(r.text, "html.parser")

    count = 0
    img_urls = []
    viewer_img = page_soup.find("div", {"class": "viewer_img"})
    for img in viewer_img.find_all("img"):
        img_url = re.sub(r'\?type=[a-zA-z0-9]+$', r'', img['data-url'])
        img_urls.append((img_url, os.path.join(directory, f"{count:03}")))
        count += 1

    with ThreadPool(processes=10) as tp:
        map_start = time.time()
        for imap_result in tp.imap_unordered(save_image, img_urls):
            print("{} - {:.2f} seconds".format(imap_result, time.time() - map_start), end="\r")
        print("{}: {} - total time: {:.2f}s".format(title, episode, time.time() - map_start))

    return 0


def save_image(data):
    image_url = data[0]
    name = data[1]

    headers = {
            'Host': 'webtoon-phinf.pstatic.net',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Accept': 'image/png,*/*',
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.webtoons.com/',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers'
    }

    with requests.get(image_url, headers=headers, stream=True) as r:
        ext = r.headers.get('content-type').split("/")[1]
        r.raise_for_status()
        with open(f"{name}.{ext}", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return name


def main():
    parser = argparse.ArgumentParser(description="Downlaods Webtoons")
    parser.add_argument('url', help='Chapter url')
    parser.add_argument("--start", type=int, help="Starting chapter")
    parser.add_argument("--end", type=float, help="Ending chapter", default=float('inf'))

    args = parser.parse_args()
    m = re.match(valid_url, args.url)

    start = int(m.group("episode_no"))
    if args.start:
        start = args.start

    errors = 0
    current = start
    while(errors < 5 and args.end + 1 > current):
        print(current, end=" --- ")
        if parse(f'https://www.webtoons.com/{m.group("language")}/{m.group("genre")}/{m.group("title_string")}/{m.group("episode_string")}/viewer?title_no={m.group("title_no")}&episode_no={current}'):
            errors += 1
        current += 1


main()
