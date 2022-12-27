from bs4 import BeautifulSoup as soup
import requests
import sys
import re
import json
import youtube_dl
import os
import json
import argparse

VALID_URL = "https://www.svtplay.se"
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def progress_hook(d):
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        sys.stdout.write("\033[K")
        print("Done downloading {}".format(file_tuple[1]))
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'], end='\r')

def format_name(title):
    title = re.sub('[?/|\\\}{:<>*"]', '', title)
    if len(title) > 190:
        title = title[:120]
    return title

def single_episode(episode_data):
    print("Episode:", episode_data["title"])
    episode_title = episode_data["title"]
    title_clean = format_name(episode_title)

    directory = os.path.join(
        BASE_DIR,
        format_name(episode_data["program"]),
        format_name(episode_data["season"]),
        title_clean
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, format_name("{}-{}.json".format(episode_data["id"], episode_title))), 'w') as f:
        json.dump(episode_data, f)
    ydl_opts = {
        'progress_hooks': [progress_hook],
        'logger': MyLogger(),
        'continuedl': True,
        'ignoreerrors': True,
        'outtmpl': os.path.join(directory, format_name("{}-{}.%(ext)s".format(episode_data["id"], episode_title)))
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([episode_data["url"]])

def single_program(path, episodes=[], page=1):
    url = VALID_URL + path 
    r = requests.get(url)
    if r.status_code == 404:
        return episodes
    page_html = r.content
    page_soup = soup(page_html, "html.parser")

    raw_data = page_soup.find("script", {"id": "__NEXT_DATA__"}).text
    data = json.loads(raw_data)

    series_info_key = ""
    series_info_keys = list(data["props"]["urqlState"].keys())
    for key in series_info_keys:
        json_data = json.loads(data["props"]["urqlState"][key]["data"])
        if not json_data.get("detailsPageByPath"):
            continue
        else:
            series_info_key = key

    series_info = data["props"]["urqlState"][series_info_key]["data"]

    series_info_json = json.loads(series_info)
    print(series_info_json["detailsPageByPath"].keys())

    with open("test.json", "w")as f:
        json.dump(series_info_json["detailsPageByPath"], f)

    seasons = series_info_json["detailsPageByPath"]["associatedContent"]
    for season in seasons:
        print("SEASON:", season["name"])
        current_episodes = season["items"]

        for episode in current_episodes:
            #print(episode["heading"], episode["item"]["urls"]["svtplay"])
            ep_data = {
                "id": episode["item"]["id"],
                "program": series_info_json["detailsPageByPath"]["heading"],
                "title": episode["heading"],
                "season": season["name"],
                "description": episode["description"],
                "url": VALID_URL + episode["item"]["urls"]["svtplay"]
            }
            episodes.append(ep_data)
    return episodes

def all_programs():
    url = VALID_URL + "/program"
    page_html = requests.get(url).content
    page_soup = soup(page_html, "html.parser")

    programs = []
    temp_programs = page_soup.find_all("a", {"class": "sc-73d4a946-4"})
    for program in temp_programs:
        print("Adding program:", program["href"])
        programs.append(program["href"])

    return programs


def scrape():
    print("Gathering all programs...")
    programs = all_programs()
    for program in programs:
        episodes = single_program(program, episodes=[])
        for episode in episodes:
            single_episode(episode)


def main ():
    parser = argparse.ArgumentParser(description="Archive all programs from Öppet arkiv")
    parser.add_argument("-o", "--output", type=str, help="Set download directory")
    args = parser.parse_args()

    global BASE_DIR
    if args.output:
        BASE_DIR = os.path.abspath(args.output)
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

    scrape()
    #episodes = single_program("/brus", episodes=[])
    #for episode in episodes:
    #    single_episode(episode)


main()