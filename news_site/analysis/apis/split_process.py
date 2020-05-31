import pandas as pd
import numpy as np
import jieba
jieba.dt.cache_file = 'jieba.cache.new'
import jieba.posseg as pseg
from tqdm import tqdm
from django.db.models import Q
from newsdb.models import New, Sentiment, Tagger
from datetime import date
import json

class Split:
    def __init__(self):
        pass

    def seperate(self, sentence):
        words = pseg.cut(sentence)
        return words

    def is_chinese(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False

    def format_str(self, content):
        content_str = ''
        for i in content:
            if self.is_chinese(i):
                content_str = content_str + ｉ
        return content_str

    def remove_covid_message(self, content):
        a = '看更多 武漢肺炎（COVID-19、新冠肺炎）疫情'
        b = 'if(!detectmob()&&'
        head, sep, tail = content.partition(a)
        head, sep, tail = head.partition(b)
        return head

    def seperate_news(self, query_set):
        news_list = []
        seperated_word_list = []
        for query in query_set:
            content = query.content
            content = self.remove_covid_message(content)
            news_list.append(content)

        chinese_list = []
        for line in news_list:
            chinese_list.append(self.format_str(line))
        i = 0
        for news in tqdm(news_list):
            temp_list = []
            words = self.seperate(news)
            for word, flag in words:
                temp_list.append((word, flag))
            seperated_word_list.append(temp_list)
            a = Tagger(news=query_set[i], split=json.dumps(temp_list), date=query_set[i].date)
            a.save()
            i += 1
        return seperated_word_list