import requests
import json
import urllib.request
import time
import os
import sys
import re

directory = os.getcwd()
folder = "metadata"

def format_name(title):
    title = re.sub('[?/|\\\}{:<>*"]', '', title)
    if len(title) > 110:
        title = title[:110]
    return title

def scrape(start, end):
    count = 0
    for page in range(start, end):
        print("Page", page)
        payload = {
            "query":{
                "text":"",
                "property":"authors",
                "dvalue":None,
                "dproperty":"librarians"
                }
        }
        r = requests.get("https://books.memoryoftheworld.org/books?page={}".format(page), data=json.dumps(payload))

        books = r.json()
        if r.status_code == 200:
            for book in books["_items"]:
                with open(os.path.join(directory, folder, "{}_{}.json".format(format_name(book["title"]), book["_id"])), 'w+') as f:
                    json.dump(book, f)
                forms = book["formats"]
                for form in forms:
                    file_path = form["dir_path"]
                    file_name = format_name(form["file_name"])
                    print(file_name)
                    application_id = str(book["_id"])
                    url = "https:{}{}{}".format(book["library_url"], file_path, file_name)
                    print("Count", count, url)
                    with open(os.path.join("books.txt"), "a+") as f:
                        f.write(str(url) + "\n")
                    count += 1
        else:
            return

def main():
    if len(sys.argv) != 3:
        sys.exit("Specify <start page> <end page>")
    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    except ValueError:
        sys.exit("Only use integers")

    if start > end:
        sys.exit("Don't be stupid")

    scrape(start, end + 1)

main()
