from time import sleep
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup as soup
import re
import os
import json
import sys

def scrape(down_path, first, last):

    if not os.path.exists(down_path):
        os.makedirs(down_path)

    for page in range(first, last):
        print("==== Page", page, "====")
        url = "https://www.artic.edu/collection?page={page}"
        req = Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
        )

        uClient = urlopen(req)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "lxml")

        listings = page_soup.find_all("li", {"class":["m-listing--variable-height", "o-pinboard__item", "s-positioned"]})
        for listing in listings:
            # print("#######################")
            # print(listing.a["href"])

            req = Request(
                listing.a["href"], 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    }
            )
            uClient = urlopen(req)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "lxml")

            image_url = page_soup.find_all("div", {"class": "m-article-header__img-container"})[0].img["data-iiifid"] + "/full/full/0/default.jpg"
            image_meta = page_soup.find_all("div", {"class": "m-article-header__img-container"})[0].img["data-iiifid"] + "/info.json"
            image_title = page_soup.find_all("span", {"class": "title"})[0].text
            dates = page_soup.find_all("p", {"class": "title"})
            image_date = dates[0].text
            try:
                image_artist_name = page_soup.find_all("dd", {"itemprop": "creator"})[0].span.a.text
                image_artist_url = page_soup.find_all("dd", {"itemprop": "creator"})[0].span.a["href"]
            except IndexError:
                image_artist_name = ""
                image_artist_url = ""
            try:
                image_artist_origin = dates[1].text.strip(image_artist_name).split(",")[0].strip()
                image_artist_date = dates[1].text.strip(image_artist_name).split(",")[1].strip()
            except IndexError:
                image_artist_origin = ""
                image_artist_date = ""
            try:
                image_origin = page_soup.find_all("dd", {"itemprop": "locationCreated"})[0].span.text
            except IndexError:
                image_origin = ""
            try:
                image_medium = page_soup.find_all("dd", {"itemprop": "material"})[0].span.text
            except IndexError:
                image_medium = ""
            try:
                description = page_soup.find_all("div", {"itemprop": "description"})[0]
            except IndexError:
                description = ""
            
            image_inscriptions = ""
            image_dimensions = ""
            image_creditline = ""
            image_reference = ""
            image_copyright = ""
            dt_tags = page_soup.find_all("h2", {"class": "f-module-title-1"})
            for dt_tag in dt_tags:
                if (dt_tag.text == "Inscriptions"):
                   image_inscriptions = dt_tag.parent.findNext("dd").span.text
                elif dt_tag.text == "Dimensions":
                    image_dimensions = dt_tag.parent.findNext("dd").span.text
                elif dt_tag.text == "Credit Line":
                    image_creditline = dt_tag.parent.findNext("dd").span.text
                elif dt_tag.text == "Reference Number":
                    image_reference = dt_tag.parent.findNext("dd").span.text
                elif dt_tag.text == "Copyright":
                    image_copyright = dt_tag.parent.findNext("dd").span.text
                

            # image_inscriptions = page_soup.find_all("span", {"class": "f-secondary"})[6].text
            # image_dimensions = page_soup.find_all("span", {"class" : "f-secondary"})[7].text
            # image_creditline = page_soup.find_all("span", {"class": "f-secondary"})[8].text
            # image_reference = page_soup.find_all("span", {"class": "f-secondary"})[9].text
            extras = page_soup.find_all("div", {"class": "o-accordion__panel"})
            image_publication_history = []
            image_exhibition_history = []
            image_provenance = []
            image_multimedia = []
            image_educational = []
            image_description = []

            # print("Title:", image_title)
            # print("Origin:", image_origin)
            # print("URL:", image_url)
            # print("Date:", image_date)
            # print("Artist Name:", image_artist_name)
            # print("Artist Origin:", image_artist_origin)
            # print("Artist Date:", image_artist_date)
            # print("Artist URL:", image_artist_url)
            # print("Medium:", image_medium)
            # print("Inscriptions:", image_inscriptions)
            # print("Dimensions:", image_dimensions)
            # print("Credit Line:", image_creditline)
            # print("Reference Number:", image_reference)

            for extra in extras:
                div_id = extra["id"]
                if div_id == "panel_publication-history":
                    image_publication_history = simple_list(extra)
                    # print("Publication History:", image_publication_history)
                elif div_id == "panel_exhibition-history":
                    image_exhibition_history = simple_list(extra)
                elif div_id == "panel_provenance":
                    try:
                        image_provenance = extra.div.p.text
                    except AttributeError:
                        image_provenance = simple_list(extra)
                elif div_id == "panel_multimedia":
                    image_multimedia = catch_list(extra)
                elif div_id == "panel_educational-resources":
                    image_educational = catch_list(extra)
            
            if description != "":
                for paragraph in description.find_all("p"):
                    image_description.append(paragraph.text)
            # print("Description:", image_description)
            print("Downloading", image_title)

            image_meta_json = requests.get(url=image_meta).json()
            
            artist = {}
            artist["name"] = image_artist_name
            artist["date"] = image_artist_date
            artist["origin"] = image_artist_origin
            artist["url"] = image_artist_url

            data = {}
            data["title"] = image_title
            data["date"] = image_date
            data["origin"] = image_origin
            data["artist"] = artist
            data["description"] = image_description
            data["medium"] = image_medium
            data["inscriptions"] = image_inscriptions
            data["dimensions"] = image_dimensions
            data["credit_line"] = image_creditline
            data["reference_number"] = image_reference
            data["copyright"] = image_copyright
            data["url"] = image_url
            data["publication_history"] = image_publication_history
            data["exhibition_history"] = image_exhibition_history
            data["provenance"] = image_provenance
            data["multimedia"] = image_multimedia
            data["educational_resources"] = image_educational
            data["metadata"] = image_meta_json

            image_filename = get_valid_filename(image_title + "_" + image_reference + "_" + image_artist_name)
            if not os.path.isfile("{}/{}.jpg".format(down_path, image_filename)):
                urlretrieve(image_url, "{}/{}.jpg".format(down_path, image_filename))
            with open("{}/{}.json".format(down_path, image_filename), "w+") as f:
                json.dump(data, f)
            
            sleep(1)
            
            

# https://github.com/django/django/blob/master/django/utils/text.py
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def simple_list(extra):
    publications = extra.find_all("li")
    info = []
    for publication in publications:
        info.append(publication.text)
    return info


def catch_list(extra):
    items = extra.find_all("li")
    info = []
    for item in items:
        try:
            media = {
                "Label": item.span.text,
                "Link": item.a["href"] 
            }
            info.append(media)
        except AttributeError:
            pass
    return info

def main():
    if len(sys.argv) != 3:
        sys.exit("Specify <first page> <last page>")
    try:
        first = int(sys.argv[1])
        last = int(sys.argv[2])
    except ValueError:
        sys.exit("Only use integers")

    if first > last:
        sys.exit("Don't be stupid")

    scrape("artworks", first, last + 1)

main()