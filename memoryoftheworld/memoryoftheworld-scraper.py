import requests
import json
import urllib.request
import os

downloaded = []
with open('downloaded.txt', "a+") as f:
  downloaded = [line.rstrip('\n') for line in f]
    
def get_books(last_id):
    payload = {
        "last_id": last_id,
        "query":{
            "text":"",
            "property":"authors",
            "dvalue":None,
            "dproperty":"librarians"
            }
    }
    r = requests.post("https://library.memoryoftheworld.org/get_books", data=json.dumps(payload))

    books = r.json()
    if r.status_code == 200:
        for book in books["books"]:
            forms = book["formats"]
            for form in forms:
                file_path = book["format_metadata"][form]["file_path"]
                file_name = book["format_metadata"][form]["file_name"]
                application_id = str(book["application_id"])
                url = book["prefix_url"] + file_path
                if application_id not in downloaded:
                    print(url)
                    with open("downloaded.txt", "a+") as f:
                        f.write(str(application_id) + "\n")
                    downloaded.append(application_id)
        get_books(books["last_id"])
    else:
        return

get_books(None)
