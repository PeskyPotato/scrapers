from time import sleep
from random import randint
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import re


def grab_papers(total = 154):
    url_page = 0
    while(url_page < total+1):
        url = 'https://waset.org/Publications?p=' + str(url_page)
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
        
        papers = page_soup.findAll("div", {"class":"publication-listing"})

        for paper in papers:
            title = paper.findAll("h5", {"class", "card-header"})[0].text

            for btn in paper.findAll("a", {"class": "btn-sm"}):
                if btn.text == 'JSON':
                    json = btn['href']
                elif btn.text == 'PDF':
                    pdf_redirect = btn['href']

            paper_id = re.findall('[0-9]+', pdf_redirect)[0]
            if(title is None):
                title = str(paper_id)
            title = formatTitle(title)
            pdf = "https://panel.waset.org/publications/{}/pdf".format(paper_id)
            print("wget -c --content-disposition -O {}.pdf {}".format(title, pdf))
            print("wget -c --content-disposition -O {}.json {}".format(title, json))
            
            sleep(randint(0,1))
        url_page += 1
        
def formatTitle(title):
    title = re.sub('[?/|\\\:<>*"]', '', title)
    title = re.sub(' ','_', title)
    if len(title) > 190:
        title = title[:189]
    return title

grab_papers()


