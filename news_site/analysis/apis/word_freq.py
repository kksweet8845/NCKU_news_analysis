from newsdb.models import Subject, Brand, Brand_sub, New, Word
from ckiptagger import data_utils, construct_dictionary, WS, POS
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import pandas as pd
import os, re
from django.conf import settings
from .hotword_v1 import Hotword




def get_word_freq(where):

    util_path = settings.BASE_DIR + '/analysis/apis/utils/ckiptagger'

    ws = WS(util_path + '/data')
    pos = POS(util_path + '/data')

    word_to_weight = {}
    with open(util_path + '/dictionary.txt', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            word_to_weight[line] = 2

    dictionary = construct_dictionary(word_to_weight)
    print(dictionary)

    word_mapping = {}
    for d in Word.objects.all():
        id = d.id
        word = d.word
        word_mapping[word] = id

    stopwords = []
    with open(util_path + '/stopwords.txt', encoding='utf8') as f:
        stopwords.extend(f.read().split())

    news = New.objects.filter(*where)

    df = pd.DataFrame(
        list(news.values()),
        columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url']
    )

    def text_preprocessing(raw):
        text = raw['content']
        tmp = re.sub(r'（.+）','', text)
        tmp = re.sub(r'〔.+〕', '', tmp)
        tmp = re.sub(r'[\r\n]', '', tmp)
        tmp = tmp.strip()
        # tmp = tmp.split(' ')
        raw['content'] = tmp
        return raw

    def value_convert(raw):
        date = raw['update_time']
        raw['update_time'] = date.strftime('%Y-%m-%d')
        raw['date'] = raw['date'].strftime('%Y-%m-%d')
        return raw

    pre_df = df \
            .apply(text_preprocessing, axis=1) \
            .apply(value_convert, axis=1)

    def day_wise(df):
        date = df['date'].tolist()
        date_dict = {}

        for d in date:
            if d not in date_dict.keys():
                date_dict[d] = []

        for row in df.iterrows():
            index = row[0]
            row = row[1]
            date_dict[row.date].append(index)

        return date_dict

    date_dict = day_wise(pre_df)

    print(date_dict)

    def clean_words(word):
        tmp = word.strip()
        tmp = re.sub(r'[^\u4e00-\u9fff]', '', tmp)
        # tmp = re.sub(r'[日月年點時號分鐘:,天間至前萬元千百公里億餘]', '', tmp)
        # tmp = re.sub(r'http(...)', '', tmp)
        tmp = re.sub(r'[0-9]+', '', tmp)
        tmp = re.sub(r'[──|─]', '', tmp)
        tmp = re.sub(r'[\r\n\b\s]', '', tmp)
        tmp = re.sub(r'[\n]', '', tmp)
        # tmp = re.sub(r'[A-Za-z]', '', tmp)
        tmp = tmp.translate(str.maketrans('', '', '《》「」！，。、：﹔｜│·※【】？▲')) ## ch
        tmp = tmp.translate(str.maketrans('', '', '!@#$%^&*()_-+[]{}/,.<>:;\"\'\\=~`|'))
        tmp = tmp.strip()
        if len(tmp) > 1:
            return tmp
        return np.nan

    def count_hotWord(content, df):
        words_ls = ws(content)
        pos_ls = pos(words_ls)

        ls = []
        for words in words_ls:
            if len(words) != 0:
                ls.append(' '.join(word for word in words if word not in stopwords))

        vec = CountVectorizer(vocabulary=word_mapping)
        count_vec = vec.transform(ls)

        all_word = Word.objects.all()

        # for row in df.iterrows():




    def tagger(content, date_dict):
        words_ls = ws(content,
                      coerce_dictionary = dictionary)
        pos_ls = pos(words_ls)
        ls = []

        pos_tag = ['Nb', 'Nc']
        for date in date_dict.keys():
            ls.append((date, []))

        for l in ls:
            date = l[0]
            dl = l[1]
            for di in date_dict[date]:
                words_series = pd.Series(words_ls[di]).apply(clean_words).dropna()
                for dw, dp in zip(words_series, pos_ls[di]):
                    if dp in pos_tag:
                        dl.append(dw)

        rst = []
        for l in ls:
            dl = l[1]
            date = l[0]
            if len(dl) != 0:
                rst.append((date,  ' '.join( [str(word) for word in dl if word not in stopwords] ) ))

        return rst

    # day wise corpus
    corpus = tagger(pre_df['content'], date_dict)

    vectorizer = TfidfVectorizer()
    try:
        tfidf_vec = vectorizer.fit_transform([dc[1] for dc in corpus])
    except ValueError:
        print(corpus)

    print(tfidf_vec.shape)
    tfidf_arr = tfidf_vec.toarray()
    sort = np.argsort(tfidf_arr, axis=1)[:, -20:]
    print(sort)
    names = vectorizer.get_feature_names()
    keywords = pd.Index(names)[sort].values
    keywords_dict = list(zip([dc[0] for dc in corpus], keywords))
    print(keywords_dict)


    def get_newsHotword(df, universe_num):
        words = ws(df['content'])
        ll = []
        for i in words:
            if len(i) != 0:
                ll.append(' '.join(word for word in i if word not in stopwords))
        vectorizer = TfidfVectorizer()
        try:
            tfidf_vec = vectorizer.fit_transform(ll)
        except ValueError:
            print(ll)

        tfidf_arr = tfidf_vec.toarray()
        sort = np.argsort(tfidf_arr, axis=1)[:, -universe_num:]
        names = vectorizer.get_feature_names()
        keywords = pd.Index(names)[sort].values
        df['keywords'] = list(keywords[:])
        ls = []
        for i in range(sort.shape[0]):
            tmp = []
            for arg in sort[i,:]:
                tmp.append(arg)
            ls.append(tmp)

        print(np.array(ls).shape)
        df['keywords_dt'] = ls

    get_newsHotword(pre_df, 20)

    def find_relative_news(keywords_ls, df):
        ls = []
        for i in keywords_ls:
            tmp = {}
            for j in i:
                tmp[j] = {}
            ls.append(tmp)
        keywords_ls_np = np.array(keywords_ls)
        key_row, key_col = keywords_ls_np.shape
        for row in df.iterrows():
            row = row[1]
            id = row.id
            news_keywords = row.keywords
            news_keywords_dt = np.array(row.keywords_dt)
            dt_sort = np.argsort(news_keywords_dt, axis=0)[-15:]
            for dr in range(key_row):
                for dc in range(key_col):
                    if keywords_ls_np[dr, dc] in news_keywords:
                        for di in dt_sort:
                            if keywords_ls_np[dr, dc] != news_keywords[di]:
                                tmp_dict = ls[dr][keywords_ls_np[dr, dc]]
                                if row.date in tmp_dict.keys():
                                    if id in tmp_dict[row.date].keys():
                                        tmp_dict[row.date][id]['keywords'].append(news_keywords[di])
                                    else:
                                        tmp_dict[row.date][id] = {}
                                        tmp_dict[row.date][id]['keywords'] = []
                                        tmp_dict[row.date][id]['url'] = row.url
                                else:
                                    tmp_dict[row.date] = {}
                                # ls[dr][keywords_ls_np[dr, dc]].append((news_keywords[di], id, row.url, row.date))
        return ls

    relative_news = find_relative_news(keywords, pre_df)

    return keywords.tolist(), relative_news







