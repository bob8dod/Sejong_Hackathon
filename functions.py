import re
import pandas as pd
from eunjeon import Mecab
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

mecab = Mecab()
# containers = ['NNG', 'NNP', 'NNB', 'NNBC', 'NR', 'NP', 'VV', 'VA', 'VX', 'VCP', 'VCN', 'MM']
# stop_words = ['JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC']
# hangul = re.compile('[^가-힣]+')
# sss_compile = re.compile('[^0-9a-zA-Z가-힣\s]')

# 분석과정
def preprocessing(review_data):
    for i in range(len(review_data)):
        review_data.loc[i, 'review'] = re.sub('[^0-9가-힣\s]', '', review_data.loc[i, 'review'])
    review_data = review_data.dropna().reset_index(drop=True)
    return review_data

def morphs_pos(review_data):
    review_data_list = []
    for i in range(len(review_data)):
        rev = mecab.pos(review_data.loc[i, 'review'])  # mecab
        review_data_list.append(rev)
    return review_data_list

def return_nouns(review_data):
    nouns = []
    for i in range(len(review_data)):
        noun = mecab.pos(review_data.loc[i, 'review'])
        f_noun = [w for w, v in noun if v == 'NNG']  # or v=='VV' or v=='VX' or v='VA
        nouns.append(f_noun)
    return nouns

def count_noun(nouns):
    vocab = dict()
    for words in nouns:
        for word in words:
            if word not in vocab:
                vocab[word] = 1
            else:
                vocab[word] += 1
    vocab_sorted = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
    return vocab_sorted

def check_vocab(t, review_data_list):
    t.fit_on_texts(review_data_list)
    vocab_size = len(t.word_index) + 1
    return vocab_size

def return_keyword(review_data):
    review_data = pd.DataFrame(review_data, columns=['review']).reset_index(drop=True)
    review_data = preprocessing(review_data)  # 전처리
    review_data_list = morphs_pos(review_data)  # 형태소 토큰화
    nouns = return_nouns(review_data)  # 명사 추출
    vocab_sorted = count_noun(nouns)  # 명사 키워드
    check_vocab = [word for word in vocab_sorted if len(word[0])>1]  # 20개 출력
    # JKS, JX_중요조사들
    # josa = ['JKS', 'JX']  # 품사 중 조사에 대한 표현 저장 #+JKO, JKB, JKG, JKV, JKC, JC
    # word_next_josa = {w: 0 for w, k in vocab_sorted}  # 단어 뒤에 조사가 붙는지에 대한 count를 저장하기 위한 딕셔너리
    # for i in range(len(review_data_list)):
    #     for word, value in vocab_sorted:  # 저장된 단어들 호출
    #         for idx in range(len(review_data_list[i])):
    #             if word == review_data_list[i][idx][0]:
    #                 if idx + 1 < len(review_data_list[i]) and review_data_list[i][idx + 1][
    #                     1] in josa:  # 해당 단어의 다음에 조사가 나온다면
    #                     word_next_josa[word] += 1  # count 해줌
    #
    # word_josa_count = sorted(word_next_josa.items(), key=lambda x: x[1], reverse=True)[:20]  # count를 기준으로 sort 20개
    # keyword_before = []
    # for i in range(len(word_josa_count)):
    #     for j in range(len(check_vocab)):
    #         if word_josa_count[i][0] == check_vocab[j][0] and word_josa_count[i][1] > 1:  # 그냥 가장 많이 나온 단어들과 다음 단어가 조사가 나오는 단어들 중 을 선택
    #             keyword_before.append(word_josa_count[i][0])

    return check_vocab[:10]

def stock_chart(stock_name, abnormal):
    time = pd.read_csv(
        "stock_data/{}.csv".format(stock_name),
        parse_dates=["Date"],
        index_col="Date"
    )
    time = time.reset_index()[['Date', 'price']]
    time.columns = ['date', 'released']

    prev = time[:-5]
    predict = time[-5:]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prev['date'], y=prev['released'], name="Stock Price"))

    fig.add_trace(go.Scatter(x=predict['date'], y=predict['released'], name="Predict"))

    fig.update_layout(plot_bgcolor='white')

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,

    ))

    # input_abnormal_detect_date
    for i in abnormal:
        fig.add_vrect(x0=i[0], x1=i[1], fillcolor="green", opacity=0.25, line_width=0)

    # fig.show()
    a = fig.to_json()
    return a, fig

# stock_name = '000270_기아'
# abnormal = [("2016-09-24", "2016-10-18"), ("2015-09-24", "2015-10-18")]
#
# a,fig = stock_chart(stock_name,abnormal)
# fig.show()
# print(a)