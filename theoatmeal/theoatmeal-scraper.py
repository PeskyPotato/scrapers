from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import os
import sys
import argparse

def scrape(start, end):
    dir = os.path.dirname(os.path.abspath(__file__))
    oatmealdir = dir +"/OatmealComics"

    if not os.path.exists(oatmealdir):
            os.makedirs(oatmealdir)

    for page in range(start, end):
        main_url = "https://theoatmeal.com/feed/index/page:" + str(page)
        print("==== Page", page, " ====")

        main_url_opener = urlopen(main_url)
        main_url_response = main_url_opener.read()

        main_url_soup = BeautifulSoup(main_url_response,"lxml")
        page_check = main_url_soup.findAll("span", {"class": "ghost"})
        if(len(page_check)):
            print("Download done")
            break

        mylist = []
        for comiclink in main_url_soup.find_all('a'):
            all_links = comiclink.get('href')
            split_links = all_links.split('/')
            try:
               if split_links[1]=="comics" and split_links[2]!="":
                    if all_links not in mylist:
                        mylist.append(all_links)

            except:
                pass

        for element in mylist:
            old_source = element
            new_source = old_source.replace('/comics/','http://theoatmeal.com/comics/')

            url = new_source

            opener = urlopen(url)
            response = opener.read()

            soupedversion = BeautifulSoup(response,"lxml")

            comicname = soupedversion.title.string
            comicname = comicname.replace('?','')
            comicname = comicname.replace(':','')
            comicname = comicname.replace('*','')
            comicname = comicname.replace('"','')

            comicdir = dir +"/OatmealComics/"+ comicname

            if not os.path.exists(comicdir):
                print ("Downloading",comicname)
                os.makedirs(comicdir)
            else:
                if not len(os.listdir(comicdir)) == 0:
                    print ("Duplicated",comicname)
                    continue
                else:
                    print ("Downloading",comicname)

            for imglink in soupedversion.find_all('img'):
                mylink =  imglink.get('src')
                current_comic_src = mylink.split('/')
                if current_comic_src[4] == "comics":
                    open_img = urlopen(mylink)
                    img_data = open_img.read()
                    filename = current_comic_src[6]
                    filename = filename.replace('?reload','')
                    path = os.path.join(comicdir,filename)
                    with open (path,"wb") as data:
                        data.write(img_data)

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
