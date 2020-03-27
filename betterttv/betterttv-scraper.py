import requests
import sys
import os
import json
import re
from multiprocessing import Pool

def scrape(offset, limit = 50):
    print("========={}========".format(offset))
    direct = os.getcwd()
    download_direct = os.path.join(direct, "emotes")
    if not os.path.exists(download_direct):
        os.makedirs(download_direct)

    url = 'https://api.betterttv.net/3/emotes/shared/top?offset={}&limit={}'.format(offset, limit)

    r = requests.get(url)
    data = r.json()
    
    for emote in data:
        name = "{}-{}.{}".format(emote["emote"]["code"], emote["emote"]["id"], emote["emote"]["imageType"])
        link = "https://cdn.betterttv.net/emote/{}/3x".format(emote["emote"]["id"])
        r_zip = requests.get(link, stream=True)
        if not os.path.exists(download_direct + name):
            print("Downloading ", name)
            with open(os.path.join(download_direct, name), "wb") as f:
                f.write(r_zip.content)
            with open(os.path.join(download_direct, emote["emote"]["code"] + ".json"), "w+") as f:
                json.dump(emote, f)

def single(url):
    re_search = re.search('https?://betterttv.com/emotes/([a-z0-9]+)$', url)
    if re_search:
        id = re_search.group(1)
        
        r = requests.get("https://api.betterttv.net/3/emotes/{}".format(id))

        data = r.json()
        download_emote({"emote":data})

def download_emote(emote):
    direct = os.getcwd()
    download_direct = os.path.join(direct, "emotes")
    if not os.path.exists(download_direct):
        os.makedirs(download_direct)

    name = "{}-{}.{}".format(emote["emote"]["code"], emote["emote"]["id"], emote["emote"]["imageType"])
    link = "https://cdn.betterttv.net/emote/{}/3x".format(emote["emote"]["id"])
    r_zip = requests.get(link, stream=True)
    if not os.path.exists(download_direct + name):
        print("Downloading ", name)
        with open(os.path.join(download_direct, name), "wb") as f:
            f.write(r_zip.content)
        with open(os.path.join(download_direct, emote["emote"]["code"] + ".json"), "w+") as f:
            json.dump(emote, f)

for i in range(0, 8000, 50):
    scrape(i)
