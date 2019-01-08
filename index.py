import sys
import urllib.request
import requests
import os
import shutil
import json
from bs4 import BeautifulSoup

if __name__ == "__main__":
    url = sys.argv[1]   # console에서 url 인자를 받아서 쓴다
    req = requests.get(url)
    file_name = url.split("=")[-1]  # 이미지나 최종 결과 저장 시 사용할 url 파라미터
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.select('body > div.l-content > ul.c-cards.js-masonry-container.content-start-line > li > a')

    img_path = './%s' % file_name   # 이미지를 저장할 폴더 생성 (이미 존재하면 덮어쓰기)
    if not os.path.exists(img_path):
        oldmask = os.umask(000)
        os.makedirs(img_path, 0o777)    # octal literals 는 0 대신에 0o나 0O를 사용해야 한대...
        os.umask(oldmask)
    else:
        shutil.rmtree('./%s' % file_name)
        oldmask = os.umask(000)
        os.makedirs(img_path, 0o777)  # octal literals 는 0 대신에 0o나 0O를 사용해야 한대...
        os.umask(oldmask)

    album_links = []
    for link in links:
        album_links.append(link.get('href'))

    discography = {}  # 앨범 순서대로 0 : {상세}, 1: {상세} 형태로 저장할 수 있도록 딕셔너리 변수를 만든다.
    for index, album_link in enumerate(album_links):
        req = requests.get(album_link)
        html = req.content          # req.text로 가져오니 문자가 깨지는 문제가 발생하여 대신 req.content 형태로 가져온다. http://ourcstory.tistory.com/78 참고
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

        album_detail = {}   # discography 의 vaule 값으로 넣어줄 변수 생성

        # 통상반 한정반 공통 정보
        title = soup.select_one(
            'body > div.l-content > div.c-disco.detail.content-start-line > div.c-disco__title').text
        release = soup.select_one(
            'body > div.l-content > div.c-disco.detail.content-start-line > div.c-disco__meta').text

        album_detail["title"] = title   # 제목 & 발매일
        album_detail["release"] = release   # 제목 & 발매일

        album_infos = soup.select('body > div.l-content > div.c-boxs.js-masonry-container > div.c-box')
        for i, album_type in enumerate(album_infos):
            cho_or_tong = album_infos[i].select_one(
                '.c-lineupHeader .c-lineupHeader__title').text.strip()  # 앨범 타입 초회한정반 or 통상
            album_detail[cho_or_tong] = {}
            album_type_details = album_infos[i].select('.c-lineupBody')  # 타입별 상세들


            for j, album_type_detail in enumerate(album_type_details):
                include = album_type_details[j].select_one('.c-lineupBody__block').text if album_type_details[
                    j].select_one('.c-lineupBody__block') else ""  # 가사집 정보
                album_detail[cho_or_tong]["include"] = include

                # cd_and_dvds = album_type_details[j].select('.c-lineupBody__heading')
                # print(cd_and_dvds[j].text)
                # track_lists = album_type_details[j].select(
                #     '.c-lineupTrackList > .c-lineupTrack > .c-lineupTrack__title')
                # track_arr = []
                # for track_list in track_lists:
                #     track_arr.append(track_list.text.strip())

                # album_detail[cho_or_tong] = {cd_and_dvds[j].text, track_arr}

            album_type_infos = album_infos[i].select('.c-lineupBody .c-lineupBody__heading')  # 타입별 상세들
            album_track_infos = album_infos[i].select('.c-lineupBody .c-lineupTrackList')  # tracklist

            track_dictionary = {}
            track_arr = []
            for at, album_track_info in enumerate(album_track_infos):
                tracks = album_track_info.select('.c-lineupTrack .c-lineupTrack__title')
                for track in tracks:
                    # print(track.text.strip())
                    track_arr.append(track.text.strip())

                track_dictionary[at] = track_arr
                track_arr = []

            for t, album_type_info in enumerate(album_type_infos):
                disk_type = album_type_info.text
                album_detail[cho_or_tong][disk_type] = {}
                album_detail[cho_or_tong][disk_type] = track_dictionary[t]


        # 각각 서브 정보들
        images = soup.select(
            'body > div.l-content > div.c-disco.detail.content-start-line > div.c-discoJackets > div.c-discoJacket > div.c-discoJacket__img > img')
        image_keys = soup.select(
            'body > div.l-content > div.c-disco.detail.content-start-line > div.c-discoJackets > div.c-discoJacket > div.c-discoJacket__name')

        for i, image_key in enumerate(image_keys):
            key = image_key.text.strip()
            img_url = images[i].get('src')
            album_detail[key]["image"] = img_url

            # 앨범 커버 저장
            img_type = img_url.split('/')[-1]
            img_file_name = "%d_%s_%s_%s" % (index, title.replace("/", ""), key.replace("/", ""), img_type)
            r = requests.get(img_url, allow_redirects=True)
            open("%s/%s" % (img_path, img_file_name), 'wb').write(r.content)        # w(write) b(binary mode)

        discography[index] = album_detail

    json_result = json.dumps(discography, ensure_ascii=False)
    result = json_result.replace('\\n', ' ').replace('\\r', ' ')

    f = open("arashi_%s.json" % file_name, "w")
    f.write(result)
    f.close()