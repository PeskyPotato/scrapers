from bs4 import BeautifulSoup as soup
import sqlite3
import requests
import sys
import re
import json
from database import Database, Speaker, Debate


def scrape(url_prefix, start, end):
    for page in range(start, end):
        url = "{}{}".format(url_prefix, page)
        print("==== Page", page, "URL", url, " ====")

        page_html = requests.get(url).content
        page_soup = soup(page_html, "html5lib")

        links = page_soup.find_all("a", {"class": "webtv-link"})
        for link in links:
            url = link['href']
            print(url)
            enter_debate(url)


def enter_debate(url):
    match = re.search("_([a-zA-Z0-9öÖÄäÅå+]+)$", url)
    if not match:
        print(f"ERROR: Cannot find dokid for {url}")
        return {}
    dokid = match.group(1)
    debate = Debate(dokid)

    r = requests.get(f"http://www.riksdagen.se/api/videostream/get/{dokid}")
    if r.status_code != requests.codes.ok:
        print(f"ERROR: Bad status code for {dokid}")
        return {}
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:
        print(f"ERROR: unable to decode {dokid}")
        return {}

    if (len(data.get("videodata")) == 0 and
            not isinstance(data.get("videodata"), list)):
        print(f"ERROR: no videodata for {dokid}")
        return {}

    if not isinstance(data.get("videodata")[0], dict):
        print(f"ERROR: no videodata dict for {dokid}")
        return {}

    debate = Debate(dokid)
    debate.title = data["videodata"][0].get("title")
    debate.debateName = data["videodata"][0]["debatename"]
    debate.debateDate = data["videodata"][0]["debatedate"]
    debate.debateType = data["videodata"][0]["debatetype"]
    debate.url = data["videodata"][0]["debateurl"]
    debate.thumbnailUrl = data["videodata"][0]["thumbnailurl"]
    debate.debateSeconds = data["videodata"][0]["debateseconds"]
    streams = data["videodata"][0]["streams"]
    if not streams:
        print(f"WARNING: No streams for {dokid}")
        return {}
    files = streams.get("files", [])
    if len(files) > 0:
        debate.streamUrl = files[0]["bandwidth"][0]["downloadurl"]

    db = Database()
    try:
        db.insert_debate(debate)
    except sqlite3.IntegrityError:
        print(f"WARNING: Debate already exists {dokid}")

    speakers = data["videodata"][0]["speakers"]
    if isinstance(speakers, list):
        for speaker in speakers:
            speaker_obj = Speaker(speaker["subid"], dokid)
            speaker_obj.start = speaker.get("start", 0)
            speaker_obj.duration = speaker.get("duration", 0)
            speaker_obj.text = speaker.get("text")
            speaker_obj.party = speaker.get("party")
            speaker_obj.number = speaker.get("number")
            speaker_obj.anfText = speaker.get("anftext")
            speaker_obj.partyCode = speaker.get("partycode")
            try:
                db.insert_speaker(speaker_obj)
            except sqlite3.IntegrityError:
                print(f"WARNING: Speaker already exists {dokid}-{speaker['subid']}")
    else:
        print(f"WARNING: No speakers for {dokid}")


def main():
    if len(sys.argv) != 4:
        sys.exit("Specify <url_prefix> <start page> <end page>")
    try:
        url_prefix = sys.argv[1]
        start = int(sys.argv[2])
        end = int(sys.argv[3])
    except ValueError:
        sys.exit("Only use integers")

    if start > end:
        sys.exit("Don't be silly")

    scrape(url_prefix, start, end + 1)


main()
