from time import sleep
from random import randint
from re import sub
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup as soup



def grab_papers():
    url_page = 0
    paper_counter = 0
    while(1):
        print("-- Grabbing page ", url_page, "Papers grabbed ", paper_counter, "--")
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
        
        papers = page_soup.findAll("div", {"class":"onePaper"})
        
        for paper in papers:
            tane = paper.findAll("div", {"class":"tane"})[0].string 
            id = paper.findAll("div", {"class":"id"})[0].string
            title = paper.findAll("div", {"class":"title"})[0].string
            if(title is None):
                title = str(id)
            json = "JSON", paper.findAll("div", {"class":"pdfButton"})[0].findAll("a", {"class":"pdf button"})[6]['href']
            pdf = "PDF", paper.findAll("div", {"class":"pdfButton"})[0].findAll("a", {"class":"pdf button"})[11]['href']
            print(paper_counter, title)

            r_pdf = requests.get(pdf[1], stream=True, headers={'User-agent': 'Mozilla/5.0'})
            with open('{}_{}_{}.pdf'.format(tane, id, formatTitle(title)), 'wb') as f:
                f.write(r_pdf.content)
            
            r_json = requests.get(json[1], stream=True, headers={'User-agent': 'Mozilla/5.0'})
            with open('{}_{}_{}.json'.format(tane, id, formatTitle(title)), 'wb') as f:
                f.write(r_json.content)
            paper_counter += 1
            sleep(randint(0,1))
        url_page += 1
        
def formatTitle(title):
    title = sub('[?/|\\\:<>*"]', '', title)
    title = sub(' ','_', title)
    if len(title) > 200:
        title = title[:199]
    return title

grab_papers()


