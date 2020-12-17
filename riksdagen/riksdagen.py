from bs4 import BeautifulSoup as soup
import sqlite3
import requests
import sys
import re
import json
import argparse
import os
from download import download_main
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
        if not links:
            print("End of {} at page {}".format(url, page))
            return


def enter_debate(url):
    match = re.search("_([a-zA-Z0-9öÖÄäÅå+]+)$", url)
    if not match:
        print(f"ERROR: Cannot find dokid for {url}")
        return {}
    dokid = match.group(1)
    debate = Debate(dokid)

    try:
        r = requests.get(f"http://www.riksdagen.se/api/videostream/get/{dokid}")
    except Exception as e:
        return {}
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
        print(f"SKIPPING: Debate already exists {dokid}")

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
                print(f"SKIPPING: Speaker already exists {dokid}-{speaker['subid']}")
    else:
        print(f"WARNING: No speakers for {dokid}")


def main():
    urls = {
        "2020": "https://riksdagen.se/sv/webb-tv/?riksmote=2020/21&p=",
        "2019": "https://riksdagen.se/sv/webb-tv/?riksmote=2019/20&p=",
        "2018": "https://riksdagen.se/sv/webb-tv/?riksmote=2018/19&p=",
        "2017": "https://riksdagen.se/sv/webb-tv/?riksmote=2017/18&p=",
        "2016": "https://riksdagen.se/sv/webb-tv/?riksmote=2016/17&p=",
        "2015": "https://riksdagen.se/sv/webb-tv/?riksmote=2015/16&p=",
        "2014": "https://riksdagen.se/sv/webb-tv/?riksmote=2014/15&p=",
        "2013": "https://riksdagen.se/sv/webb-tv/?riksmote=2013/14&p=",
        "2012": "https://riksdagen.se/sv/webb-tv/?riksmote=2012/13&p=",
        "2011": "https://riksdagen.se/sv/webb-tv/?riksmote=2011/12&p=",
        "2010": "https://riksdagen.se/sv/webb-tv/?riksmote=2010/11&p=",
        "2009": "https://riksdagen.se/sv/webb-tv/?riksmote=2009/10&p=",
        "2008": "https://riksdagen.se/sv/webb-tv/?riksmote=2008/09&p=",
        "2007": "https://riksdagen.se/sv/webb-tv/?riksmote=2007/08&p=",
        "2006": "https://riksdagen.se/sv/webb-tv/?riksmote=2006/07&p=",
        "2005": "https://riksdagen.se/sv/webb-tv/?riksmote=2005/06&p=",
        "2004": "https://riksdagen.se/sv/webb-tv/?riksmote=2004/05&p=",
        "2003": "https://riksdagen.se/sv/webb-tv/?riksmote=2003/04&p=",
        "2002": "https://riksdagen.se/sv/webb-tv/?riksmote=2002/03&p=",
        "2001": "https://riksdagen.se/sv/webb-tv/?riksmote=2001/02&p=",
        "2000": "https://riksdagen.se/sv/webb-tv/?riksmote=2000/01&p="
    }
    parser = argparse.ArgumentParser(description="Archive debates from riksdagen.se")
    parser.add_argument("--start", type=int, help="Starting page", default=1)
    parser.add_argument("--end", type=int, help="Ending page", default=200)
    parser.add_argument("--update", type=str, help="Year (2XXX) or all")
    parser.add_argument("-o", "--output", type=str, help="Set download directory")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.realpath(__file__))
    if args.output:
        base_dir = os.path.abspath(args.output)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

    if args.start > args.end:
        sys.exit("Don't be silly, the start page cannot be greater than the end page.")
    if args.update == "all":
        for year in urls.keys():
            scrape(urls[year], args.start, args.end + 1)
    elif args.update == "db_check":
        download_main(base_dir)
        return
    elif urls.get(args.update):
        scrape(urls[args.update], args.start, args.end + 1)
    else:
        print("Incorrect parameters")

    download_main(base_dir)


main()
