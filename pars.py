import requests
import os
from bs4 import BeautifulSoup
import sqlite3
import random

urls = ["http://anime.reactor.cc/tag/Anime+Ero+Ass/new",
        "http://anime.reactor.cc/tag/Anime+Ero/new",
        "http://anime.reactor.cc/new",
        "http://anime.reactor.cc/tag/Anime+Ero+Pantsu/new",
        "http://anime.reactor.cc/tag/Megane",
        "http://anime.reactor.cc/tag/Anime+Original",
        "http://mfxgs3lf.ojswcy3un5zc4y3d.cmle.ru/tag/%D0%AD%D1%82%D1%82%D0%B8/new",
        "http://anime.reactor.cc/tag/Anime+Ero+Gifs/new"]

num_url = 3

img_c = sqlite3.connect(str('notes.db'))
cursor_i = img_c.cursor()

def get_old():
    cursor_i.execute("SELECT name FROM imgs ORDER BY name DESC")
    ld_list1 = cursor_i.fetchall()
    old=[]
    for i in ld_list1:
        old.append(i[0])
    return(old)



def pars(log=False, url = 'http://anime.reactor.cc/new'):
    r = requests.get(url)
    if log:
        print(f"[log] Requests status: {r.status_code}")
    soup = BeautifulSoup(r.text)
    item = soup.find_all('a', {'class': 'prettyPhotoLink'})
    item2 = soup.find_all('a', {'class': 'video_gif_source'})
    item[len(item):] = item2

    links=[]

    for i in item:
        links.append(i.get('href'))
        if log:
            print(f"[log] Link {i.get('href')}")
    links.pop(0)
    return(links)

def downloader(log=False):

    for i in range(num_url):
        try:
            links = pars(log=log, url=urls[random.randint(0, len(urls))])
        except:
            links = pars(log=log, url=urls[random.randint(0, len(urls))])

        for i in links:
            r = requests.get(i, allow_redirects=True)
            old_list = get_old()
            if i[(i.rfind('-')+1):] in old_list:
                if log:
                    print(f"{i[(i.rfind('-') + 1):]} was download last!")
            else:
                open(f"img/{i[(i.rfind('-')+1):]}", 'wb').write(r.content)
                cursor_i.execute(f'INSERT INTO imgs VALUES (?)', (i[(i.rfind('-')+1):],))
                img_c.commit()

                if log:
                    print(f"{i[(i.rfind('-')+1):]} download!")
    return(True)

#print(downloader(log=True))


