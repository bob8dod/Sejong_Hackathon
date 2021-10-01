import requests
from bs4 import BeautifulSoup
from functions import return_keyword
from home.models import StockModel
from wordcloud import WordCloud
from collections import Counter


def Crawling(search_text,start_date,end_date):
    titles=[]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

    for i in range(1,201,10):
        try:
            url_basic = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=3&ds={}&de={}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from20210810to20210814,a:all&start={}'.format(search_text,start_date,end_date,i)

            data = requests.get(url_basic, headers=headers)
            soup = BeautifulSoup(data.text, 'html.parser')

            news_titles = soup.find_all('a',attrs={'class':'news_tit'})

            for title in news_titles:
                titles.append([title['title'], title['href']])
        except:
            pass

    return titles

stock = '삼성전자'
search_text = '{}+주식'.format(stock)
# 검색 키워드 형식 -> 1) +주식, -주식, 주식 | 하락,  "이재용 출소", 섞어서 사용가능
start_date = '2021.08.10'
end_date = '2021.08.14'

only_title=[]
for title in Crawling(search_text,start_date,end_date):
    only_title.append(title[0])
    print(title)
print(return_keyword(only_title))