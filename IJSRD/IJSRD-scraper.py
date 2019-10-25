import time
from bs4 import BeautifulSoup as soup
from multiprocessing import Pool
import requests
import json
import re
import sys
import os

def grab_papers(volume=1, issue=1, start=0):
    base_directory = os.getcwd()
    start_time = time.time()
    while(1):
        pdfs = []
        print("Volume", volume, "Issue", issue, "Start", start)
        folders = os.path.join(base_directory, "volume_{}".format(volume),
                                "issue_{}".format(issue))
        if not os.path.exists(folders):
            os.makedirs(folders)

        url = 'http://ijsrd.com/index.php?p=Archive&v={}&i={}&start={}'.format(volume, issue, start)

        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }
        page_html = requests.get(url, headers = headers).content

        page_soup = soup(page_html, "html5lib")
        papers = page_soup.findAll("tr", class_=["dark", "light"])

        if len(papers) == 0 and start != 0:
            start = 0
            issue += 1

        elif len(papers) == 0 and start == 0:
            issue = 1
            volume += 1
        elif len(papers) == 0 and start == 0 and issue == 0:
            print("Volume", volume, "Issue", issue, "Start", start)
            print("Complete")
            print("--- %s seconds ---" % (time.time() - start_time))
            sys.exit(0)
        elif len(papers) == 0:
            print("Volume", volume, "Issue", issue, "Start", start)
            print("Undocumented case")
            sys.exit(1)
        else:
            for paper in papers:
                data = {}
                paper = paper.findAll("td")[1]
                data['title'] = paper.find("a").text
                data['author'] = (re.sub('\s+', ' ', paper.text.replace(data['title'], "").split("Abstract")[0].strip()))
                data['article_url'] = paper.find("a")["href"]
                for a in paper.findAll("a", {"class", "myButton_small"}):
                    if a.text == "Download":
                        data['pdf_url'] = a["href"]
                data['abstract'] = paper.find("p", {"style": "height:75px;overflow:hidden"}).text
                pdf_id = data['pdf_url'].split("/")[-1]

                print(data["title"][:30], data['pdf_url'])
                with open(os.path.join(folders, pdf_id[:-4] + ".json"), "w") as f:
                    json.dump(data, f)
                
                pdfs.append((data["pdf_url"], folders))
                # download((data['pdf_url'], folders))
            
            start += 50
        
        pool = Pool(processes=4)
        pool.map(download, pdfs)
        pool.close()
        pool.join()

def download(param):
    print(param[0])
    r = requests.get(param[0], stream = True)
    with open(os.path.join(param[1], param[0].split("/")[-1]), "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

grab_papers()
