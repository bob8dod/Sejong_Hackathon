from django.shortcuts import render, redirect
from .models import *
from functions import *


def start_main(request):
    if request.method == 'GET':
        stocks = StockModel.objects.all()
        stock_list = []
        for stock in stocks:
            stock_list.append([stock.stock_name, stock.stock_rate, stock.stock_logo_img])

        select = StockModel.objects.get(stock_name='현대차')
        stock_num = select.stock_code
        print(stock_num)
        abnormals = Abnormal.objects.filter(stock_model=select.id)
        title_urs = []
        for abnormal in abnormals:
            if abnormal.idx == 0:
                title_url = abnormal.related_news_title_url

                img_src = abnormal.related_news_wordcloud
            title_urs.append([])
        pred_rate = select.stock_rate
        print(title_url)
        a, fig = stock_chart(stock_num, [['2012-04-04', '2012-04-20'],
                                         ['2012-11-06', '2012-11-07'],
                                         ['2013-04-23', '2013-04-24'],
                                         ['2014-09-22', '2014-10-23'],
                                         ['2018-12-04', '2019-01-02'],
                                         ['2020-04-03', '2020-06-26'],
                                         ['2020-07-16', '2020-09-04'],
                                         ['2021-01-11', '2021-02-04']], pred_rate=-0.05)
        print(a)
        print(title_url)
        title_url = ['[마감시황] 코스피 1970선 뒷걸음‥화학주 어닝쇼크', '코스피 1970선 뒷걸음‥화학주 어닝쇼크','한국항공우주 민영화 기대감에 기관 눈독','배당은 회사가 주주에게 주는 이익분배금']
        return render(request, 'main.html',
                      {'stock_list': stock_list, 'a_json': a, 'select': select, 'title_url': title_url,
                       'img_src': img_src})
