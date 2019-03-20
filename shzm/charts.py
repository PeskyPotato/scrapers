import requests
import json
import sys
import datetime
import os
import schedule
from time import sleep

# set to run every "n" hours
HOURS = 12

def top_fifty(listid, country, city):
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }

    url  = "https://www.shazam.com/shazam/v2/en-US/US/web/-/tracks/{}?pageSize=50&startFrom=0".format(listid)
    r = requests.get(url, headers)
    tracks = r.json()

    rank = 1
    for track in tracks["chart"]:
        title = track["heading"]["title"]
        artist = track["heading"]["subtitle"]
        track_key = track["key"]

        track_url = "https://www.shazam.com/shazam/v1/en-US/US/web/-/tagcounts/track/{}".format(track_key)

        track_r = requests.get(track_url, headers)
        shazams = track_r.json()["total"]
        print(title, artist, shazams)
        with open("chart.csv", "a") as f:
            f.write(datetime.datetime.now().strftime("%d-%m-%Y") + "," + country + "," + city + "," + str(rank) + "," + title + "," + artist + "," + str(shazams) + "\n")
        rank += 1

def parse():
    country_name = "portugal"
    city_name = "lisbon"

    if len(sys.argv) == 3:
        country_name = sys.argv[1].lower()
        country_name = country_name.replace("-", " ")
        city_name = sys.argv[2].lower()
        city_name = city_name.replace("-", " ")

    with open("country-city.json") as f:
        data = json.load(f)

    for country in data["countries"]:
        if country["name"].lower() == country_name.lower():
            for city in country["cities"]:
                if city["name"].lower() == city_name.lower():
                    return (city["listid"], country_name, city_name)

def main ():
    if not os.path.isfile("chart.csv"):
        with open("chart.csv", "w") as f:
            f.write("date,country,city,rank,song,artist,shazams\n")
    data = parse()
    top_fifty(data[0], data[1], data[2])


schedule.every(HOURS).hours.do(main)
while True:
    schedule.run_pending()
    sleep(1)