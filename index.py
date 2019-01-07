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

    discograpy = {}  # 앨범 순서대로 0 : {상세}, 1: {상세} 형태로 저장할 수 있도록 딕셔너리 변수를 만든다.
    for index, album_link in enumerate(album_links):
        req = requests.get(album_link)
        html = req.content          # req.text로 가져오니 문자가 깨지는 문제가 발생하여 대신 req.content 형태로 가져온다. http://ourcstory.tistory.com/78 참고
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
