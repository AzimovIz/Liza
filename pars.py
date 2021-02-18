import requests
from bs4 import BeautifulSoup
urls = ["http://anime.reactor.cc/tag/Anime+Ero+Ass/new",
        "http://anime.reactor.cc/tag/Anime+Ero+Pantsu/new",
        "http://anime.reactor.cc/tag/Anime+Ero+Gifs/new"]

def pars(log=False, url = 'http://reactor.cc'):
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
    for l in urls:
        links = pars(log=log, url=l)
        for i in links:
            r = requests.get(i, allow_redirects=True)

            open(f"img/{i[(i.rfind('-')+1):]}", 'wb').write(r.content)

            if log:
                print(f"{i[(i.rfind('-')+1):]} download!")
    return(True)

#print(downloader(log=True))


