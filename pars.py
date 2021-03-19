import requests
import os
from bs4 import BeautifulSoup
import sqlite3
import random
import threading
threading.TIMEOUT_MAX = 60*6,0

urls = ["http://anime.reactor.cc/tag/Anime+Ero+Ass/new",
        "http://anime.reactor.cc/tag/Anime+Ero/new",
        "http://anime.reactor.cc/tag/Anime+Ero+Pantsu/new",
        "http://anime.reactor.cc/tag/Anime+Ero+Pussy/new",
        "http://http://anime.reactor.cc/tag/Anime+Ero+BDSM/new",
        "http://anime.reactor.cc/tag/Megane/new",
        "http://anime.reactor.cc/tag/Anime+Original/new",
        "http://mfxgs3lf.ojswcy3un5zc4y3d.cmle.ru/tag/%D0%AD%D1%82%D1%82%D0%B8/new",
        "http://anime.reactor.cc/tag/Anime+Ero+Gifs/new"]



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

def dw(i, log = False):
    s = str(i[(i.rfind('-') + 1):])
    r = requests.get(i, allow_redirects=True)
    img_c = sqlite3.connect(str('notes.db'))
    cursor_i = img_c.cursor()
    try:
        cursor_i.execute(f'INSERT INTO imgs VALUES (?)', (s,))
        img_c.commit()
        with open(f"img/{s}", 'wb') as file:
            file.write(r.content)
            if log:
                print(f"{s} download!")
    except:
        if log:
            print(f"{s} was download last!")

def downloader(log=False, num_url = len(urls)):
    random.shuffle(urls)
    for i in range(num_url):
        try:
            links = pars(log=log, url=urls[i])
        except:
            links = pars(log=log, url=urls[i])

        for i in links:
            #s = str(i[(i.rfind('-') + 1):])
            #r = requests.get(i, allow_redirects=True)
            thread = threading.Thread(target=dw, args=[i, log])
            thread.start()


        '''for i in links:
            s = str(i[(i.rfind('-') + 1):])
            r = requests.get(i, allow_redirects=True)
            try:
                cursor_i.execute(f'INSERT INTO imgs VALUES (?)', (s,))
                img_c.commit()
                thread = threading.Thread(target=dw, args=[s, r, log])
                thread.start()
            except:
                if log:
                    print(f"{s} was download last!")'''

    return(True)

#print(downloader(log=True))


