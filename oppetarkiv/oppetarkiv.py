from bs4 import BeautifulSoup as soup
import requests
import sys
import re
import json
import youtube_dl
import os
import json
import argparse

VALID_URL = "https://www.oppetarkiv.se"
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

def single_episode(path):
    print("Episode:", path)

    page_html = requests.get(VALID_URL + path).content
    page_soup = soup(page_html, "html.parser")

    data_list = page_soup.find("dl", {"class": "svtoa-data-list"})
    dd_list = data_list.findChildren("dd")
    row = 0
    ep_data = {}
    for data in data_list.findChildren("dt"):
        data_text = data.text
        if data_text == "Titel:":
            ep_data['titel'] = dd_list[row].a.text
        elif data_text == "Genre:":
            ep_data['genre'] = dd_list[row].a.text
        elif data_text == "år:":
            ep_data['year'] = dd_list[row].a.text
        elif data_text == "Övrigt:":
            ep_data['övrigt'] = dd_list[row].a.text
        row += 1
    
    episode_title = page_soup.find("span", {"class": "svt-heading-s svt-display-block"})
    if episode_title:
        ep_data["avsnitt_titel"] = episode_title.text.strip()
    
    data =  page_soup.find("span", {"class": "svt-video-meta"}).findChildren("strong")
    if len(data) == 1:
        if "min" in data[0].text or "sek" in data[0].text:
            ep_data["längd"] = data[0].text
            ep_data["sändes"] = "Saknar sändningsdatum"
    elif len(data) == 2:
        ep_data["sändes"] = data[0].time['datetime']
        ep_data["längd"] = data[1].text

    description = page_soup.find("div", {"class": "svtContainerMain-Alt svtContainerMain-Alt--top-border svt-margin-bottom-0px"})
    ep_data["beskrivning"] = str(description)

    ep_id = re.search(r'\/video\/(?P<ep_id>[0-9]*)\/?', path).group('ep_id')
    ep_data['id'] = ep_id

    episode_title = ep_data.get("avsnitt_titel", "Ingen_avsnitt")
    title_clean = format_name(ep_data.get("titel", "Ingen_showtitel"))

    directory = os.path.join(BASE_DIR, title_clean)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, format_name("{}-{}.json".format(ep_id, episode_title))), 'w') as f:
        json.dump(ep_data, f)

    ydl_opts = {
        'progress_hooks': [progress_hook],
        'logger': MyLogger(),
        'continuedl': True,
        'ignoreerrors': True,
        'outtmpl': os.path.join(directory, format_name("{}-{}.%(ext)s".format(ep_id, episode_title)))
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([VALID_URL+path])

def single_program(path, episodes=[], page=1):
    # print("Path: {} | Episodes: {} | Page: {}".format(path, episodes, page))
    url = VALID_URL + path + "?sida={}&sort=tid_stigande?embed=true".format(page)
    r = requests.get(url)
    if r.status_code == 404:
        return episodes
    page_html = r.content
    page_soup = soup(page_html, "html.parser")

    current_episodes = page_soup.find_all("a", {"class": "svtLink-Discreet-THEMED svtJsLoadHref"})
    for episode in current_episodes:
        episodes.append(episode["href"])
    return single_program(path, episodes=episodes, page= page + 1)

def all_programs():
    url = VALID_URL + "/program"
    page_html = requests.get(url).content
    page_soup = soup(page_html, "html.parser")

    programs = []
    temp_programs = page_soup.find_all("a", {"class": "svtoa-anchor-list-link"})
    for program in temp_programs:
        programs.append(program["href"])

    return programs


def scrape():
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


main()