from django.conf import settings
from newsdb.models import New, Word
import pandas as pd
import numpy as np
from ckiptagger import data_utils, WS
import os, re


util_path = settings.BASE_DIR + '/analysis/apis/utils/ckiptagger'

class WordMap:
    def __init__(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        print(util_path)
        self.WS = WS(util_path+'/data')
        self.stopwords = []
        with open(util_path + '/stopwords.txt', encoding='utf8') as f:
            self.stopwords.extend(f.read().split())

    def text_preprocessing(self, raw):
        text = raw['content']
        tmp = re.sub(r'（.+）','', text)
        tmp = re.sub(r'〔.+〕', '', tmp)
        tmp = re.sub(r'[\r\n]', '', tmp)
        tmp = tmp.strip()
        # tmp = tmp.split(' ')
        raw['content'] = tmp
        return raw

    def fetch_news(self, where):
        news = New.objects.filter(*where)

        self.df = pd.DataFrame(
            list(news.values()),
            columns=['id',
                     'title',
                     'content',
                     'author',
                     'brand_id',
                     'sub_id',
                     'date',
                     'update_time',
                     'url']
        )

        self.pre_df = self.df \
                        .apply(self.text_preprocessing, axis=1)
        return self.pre_df

    def clean_words(self, word):
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

    def gen_dict(self, df):

        ll = []
        for article in df['content']:
            sentences = article.split('。')
            # ll = pd.concat([ll, pd.Series(sentences)])
            words_lss = self.WS(sentences)
            for dw in words_lss:
                ll.extend(dw)

        words = pd.Series(ll).apply(self.clean_words).dropna()
        words = np.unique(words.to_numpy())
        words = pd.Series(words)
        return words

