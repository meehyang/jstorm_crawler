# jstorm_crawler
아라시 앨범 정리용 크롤러

아라시 앨범 노가다로 정리하다 힘들어서 만든 파일 하나짜리 심플 python 크롤러.

git clone 해서 소스 복사 후


~~~
pip install -r requirement.txt
~~~

로 필요한 패키지 설치 

실행은

~~~
python index.py <주소값>
~~~

주소값은 각각

- 싱글 : https://www.j-storm.co.jp/arashi/discography?discography=single
- 정규 : https://www.j-storm.co.jp/arashi/discography?discography=album
- DVD : https://www.j-storm.co.jp/arashi/discography?discography=video

을 넣어주면 json 파일로 앨범 정보가 정리되고 커버 이미지 파일이 추출된다.


단...
jstorm이 퍼블리싱을 바꾸지 않아야만 유효하다...
