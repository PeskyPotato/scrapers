from bs4 import BeautifulSoup as soup
from tqdm.auto import tqdm
from multiprocessing.pool import ThreadPool
import requests
import argparse
import os


def download(in_args):
    eg_file = in_args[0]
    eg_link = in_args[1]
    if not os.path.isfile(eg_file):
        response = requests.get(eg_link, stream=True)
        with tqdm.wrapattr(open(eg_file+".part", "wb"), "write", miniters=1,
                        total=int(response.headers.get('content-length', 0)),
                        desc=eg_file[-20:]) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
        os.rename(eg_file + ".part", eg_file)

def scrape(base_dir):
    url = "http://data.riksdagen.se/data/dokument/"

    page_html = requests.get(url).content
    page_soup = soup(page_html, "lxml")

    document_urls = []
    documents = page_soup.find_all("ul", {"class": "dropdown-menu formats"})
    for document in documents:
        for link in document.find_all("a"):
            link_text = link["href"]
            if "sql" in link_text or "html" in link_text:
                file_location = os.path.join(base_dir, os.path.basename(link_text))
                if "bet-" in link_text:
                    file_location = os.path.join(base_dir, "Betänkande", os.path.basename(link_text))
                elif "ds-" in link_text:
                    file_location = os.path.join(base_dir, "Departementsserien", os.path.basename(link_text))
                elif "EUN-" in link_text:
                    file_location = os.path.join(base_dir, "EUN", os.path.basename(link_text))
                elif "f-lista-" in link_text:
                    file_location = os.path.join(base_dir, "Föredragningslista", os.path.basename(link_text))
                elif "fpm" in link_text:
                    file_location = os.path.join(base_dir, "Faktapromemoria", os.path.basename(link_text))
                elif "frsrdg-" in link_text:
                    file_location = os.path.join(base_dir, "Framställning-redogörelse", os.path.basename(link_text))
                elif "ip-" in link_text:
                    file_location = os.path.join(base_dir, "Interpellation", os.path.basename(link_text))
                elif "kammakt-" in link_text:
                    file_location = os.path.join(base_dir, "kammakt", os.path.basename(link_text))
                elif "kom-" in link_text:
                    file_location = os.path.join(base_dir, "KOM", os.path.basename(link_text))
                elif "mot-" in link_text:
                    file_location = os.path.join(base_dir, "Motion", os.path.basename(link_text))
                elif "prop-" in link_text:
                    file_location = os.path.join(base_dir, "Proposition", os.path.basename(link_text))
                elif "prot-" in link_text:
                    file_location = os.path.join(base_dir, "Protokoll", os.path.basename(link_text))
                elif "diarium " in link_text:
                    file_location = os.path.join(base_dir, "Riksdagens_diarium", os.path.basename(link_text))
                elif "rskr-" in link_text:
                    file_location = os.path.join(base_dir, "Riksdagsskrivelse", os.path.basename(link_text))
                elif "gor-" in link_text:
                    file_location = os.path.join(base_dir, "Skriftliga_frågor", os.path.basename(link_text))
                elif "sou-" in link_text:
                    file_location = os.path.join(base_dir, "Statens_offentliga_utredningar", os.path.basename(link_text))
                elif "t-lista-" in link_text:
                    file_location = os.path.join(base_dir, "Talarlista", os.path.basename(link_text))
                elif "Utredningar-" in link_text:
                    file_location = os.path.join(base_dir, "Utredningar", os.path.basename(link_text))
                elif "utskottsdokument-" in link_text:
                    file_location = os.path.join(base_dir, "Utskottsdokument", os.path.basename(link_text))
                elif "yttr-" in link_text:
                    file_location = os.path.join(base_dir, "Yttrande", os.path.basename(link_text))
                elif "vrigt-" in link_text:
                    file_location = os.path.join(base_dir, "Övrigt", os.path.basename(link_text))
                elif "samtr-" in link_text:
                    file_location = os.path.join(base_dir, "samtr", os.path.basename(link_text))

                if not os.path.exists(os.path.split(file_location)[0]):
                    os.makedirs(os.path.split(file_location)[0])

                document_urls.append((file_location, "https:" + link_text))

    return document_urls

def main():
    parser = argparse.ArgumentParser(description="Archive documents from riksdagen.se")
    parser.add_argument("-o", "--output", type=str, help="Set download directory")
    parser.add_argument("-p", "--processes", type=int, help="Set number of concurrent downloads")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.realpath(__file__))
    if args.output:
        base_dir = os.path.abspath(args.output)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

    processes = 4
    if args.processes:
        processes = args.processes

    urls = scrape(base_dir)
    with ThreadPool(processes=processes) as tp:
        for imap_result in tp.imap_unordered(download, urls):
            pass

main()
