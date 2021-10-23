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
