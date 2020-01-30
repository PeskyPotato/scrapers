#!/usr/bin/env python3

from bs4 import BeautifulSoup as soup
from urllib.request import Request
from urllib.request import urlopen
import sqlite3
import os
import sys
import html

def init_db():
    conn = sqlite3.connect('emoji.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    c.execute('CREATE TABLE IF NOT EXISTS `category` ( `CategoryID` INTEGER NOT NULL, `ParentCategoryID` INTEGER, `CategoryName` TEXT, PRIMARY KEY(`CategoryID`) )')
    c.execute('CREATE TABLE IF NOT EXISTS "emoji" ( `Code` TEXT NOT NULL UNIQUE, `Emoji` TEXT NOT NULL UNIQUE, `CLDR` TEXT NOT NULL UNIQUE, `CategoryID` INTEGER NOT NULL DEFAULT 1, PRIMARY KEY(`Code`), FOREIGN KEY(`CategoryID`) REFERENCES `category`(`CategoryID`) )')
    return (conn, c)

def close_db(conn, c):
    c.close()
    conn.close()

def check_category(conn, c, name):
    c.execute('SELECT EXISTS(SELECT `CategoryID` FROM category WHERE CategoryName=?)', (name,))
    return c.fetchone()[0]

def get_category(conn, c, name):
    ret = 0
    if check_category(conn, c, name):
        c.execute('SELECT CategoryID, ParentCategoryID FROM category WHERE CategoryName=?', (name,))
        ret = c.fetchone()
    else:
        # insert_category(conn, c, name):
        pass
    return ret

def insert_category(conn, c, name, parent=None):
    try:
        c.execute('INSERT INTO category (ParentCategoryID, CategoryName) VALUES (?,?)', (parent, name))
        conn.commit()
    except sqlite3.IntegrityError as err:
        print(err)
        sys.exit(1)

def insert_emoji(conn, c, code, emoji, cldr, category):
    c.execute('INSERT INTO emoji (Code, Emoji, CLDR, CategoryID) VALUES (?, ?, ?, ?)', (code, emoji, cldr, category))
    conn.commit()

def scrape(conn, c):
    item_data = []
    url = "https://unicode.org/emoji/charts/full-emoji-list.html"

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

    page_soup = soup(open(url), "lxml")
    items = page_soup.findAll("tr")
    parent_category = None
    category = None
    for item in items:
        tds = item.findAll("td")
        if tds:
            code = tds[1].text
            emoji = tds[2].text
            cldr = tds[-1].text
            print(parent_category, "->", category, code, emoji, cldr)
            insert_emoji(conn, c, code, emoji, cldr, get_category(conn, c, category)[0])
        elif item.th.has_attr("class"):
            if item.th.get("class")[0] == "bighead":
                parent_category = html.unescape(item.a.text)
                insert_category(conn, c, parent_category)
                print(parent_category)
            elif item.th.get("class")[0] == "mediumhead":
                category = html.unescape(item.a.text)
                insert_category(conn, c, category, get_category(conn, c, parent_category)[0])
                print(parent_category, "->", category)
            else:
                pass

def main():
    conn, c = init_db()
    scrape(conn, c)
    close_db(conn, c)

main()