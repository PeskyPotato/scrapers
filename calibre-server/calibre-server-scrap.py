from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlsplit
from urllib.error import HTTPError
import requests
import sys
import os
from lxml import etree

def scrap_mobile(page, url, direct):
    soup = BeautifulSoup(page, "html.parser")
    tags = soup.find_all("span", class_="button")

    counter = 0
    for tag in tags:
        link = tag.find('a').attrs['href']
        print(link)
        
        # urlretrieve(url + link, direct + link.split('/')[-1].replace('%20', '_').replace('%2C', ',').replace('%5B', ']').replace('%5D', ']').replace('%27', '\''))
        r = requests.get(url + link, stream = True)
        with open(direct + link.split('/')[-1].replace('%20', '_').replace('%2C', ',').replace('%5B', ']').replace('%5D', ']').replace('%27', '\''), "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    

        counter += 1

    print("Downloaded", counter, "out of", len(tags))

def scrap_xml(url, direct):
    html = urlopen(url+"/xml?_=1545645874401&start=0&num=20000&sort=date&order=descending")
    root = etree.parse(html)
    books = root.xpath('//book')

    counter = 0
    for book in books:
        id = book.get('id')
        formats = book.get('formats').split(',')
        author_sort = book.get('author_sort')
        safe_title = book.get('safe_title')
        print ("id: "+id+"  =  "+author_sort+" / "+safe_title+"  ["+','.join(formats)+"] ")
        for format in formats:
            urlretrieve(url+"/get/"+format.lower()+"/"+id, author_sort+" - "+ safe_title +"."+format.lower())
            counter += 1

    print("Downloaded", counter, "out of", len(tags))


def main ():
    method = 0

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("Enter url as arg")
        exit()

    # validate and prepare url
    if "http" not in url:
        url = "http://" + url
    url = urlsplit(url)[0] + "://" + urlsplit(url)[1]
    if url[-1] is '/':
        url = url[0:-1]

    q_page = url + '/mobile?num=10000&search=&sort=date&order=descending'

    direct = os.getcwd()
    direct = direct + '/' + url.split('//')[1] + '/'
    if not os.path.exists(direct):
        os.makedirs(direct)

    try:
        page = urlopen(q_page)
    except HTTPError:
        scrap_xml(url, direct)
        method = 1

    if (method is 0):
        scrap_mobile(page, url, direct)

if __name__ == '__main__':
    main()

