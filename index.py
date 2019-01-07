import sys
import requests
import json
from bs4 import BeautifulSoup

if __name__ == "__main__":
    url = sys.argv[1]   # console에서 url 인자를 받아서 쓴다
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.select('body > div.l-content > ul.c-cards.js-masonry-container.content-start-line > li > a')

    album_links = []
    for link in links:
        album_links.append(link.get('href'))

