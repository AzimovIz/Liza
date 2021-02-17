import requests
from bs4 import BeautifulSoup


def pars(log=False, url = 'http://anime.reactor.cc'):
    r = requests.get(url)
    if log:
        print(f"[log] Requests status: {r.status_code}")
    soup = BeautifulSoup(r.text)
    item = soup.find_all('a', {'class': 'prettyPhotoLink'})

    links = []
    for i in item:
        links.append(i.get('href'))
        if log:
            print(f"[log] Link {i.get('href')}")
    links.pop(0)
    return(links)

def downloader(links, log=False):
    for i in links:
        r = requests.get(i, allow_redirects=True)

        open(f"img/{i[(i.rfind('-')+1):]}", 'wb').write(r.content)

        if log:
            print(f"{i[(i.rfind('-')+1):]} download!")
    return(True)

#print(downloader(pars(log=True), log=True))


