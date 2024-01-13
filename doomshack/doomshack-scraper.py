from bs4 import BeautifulSoup as soup
import requests
import time
import argparse


def scrape(no_of_files, file_type):
    url = f"https://doomshack.org/uploadlist.php?n={no_of_files}&type={file_type}"
    url_base = "https://doomshack.org"

    page_response = requests.get(url)
    page_soup = soup(page_response.content, "html5lib")
    li_list = page_soup.find_all("li")

    f = open(f"{time.time()}-{no_of_files}-{file_type}.txt", "w+")

    for li in li_list:
        url_e = li.find("a")
        if url_e:
            f.write(url_base + url_e["href"] + '\n')
    f.close()
def main():
    parser = argparse.ArgumentParser(description="Get list of file urls from doomshack.org")
    parser.add_argument("--files", type=int, help="Total number of files", default=10000)
    parser.add_argument("--type", type=str, help="Type of file, zip or wad", default="wad")
    args = parser.parse_args()

    if (args.type != "wad")  and (args.type != "zip"):
        print("Please use a correct file type: zip or wad")
        exit()

    scrape(args.files, args.type)

main()
