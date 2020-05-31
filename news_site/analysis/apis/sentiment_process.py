import pandas as pd
import numpy as np
import jieba
jieba.dt.cache_file = 'jieba.cache.new'
import jieba.posseg as pseg
from tqdm import tqdm
from django.db.models import Q
from newsdb.models import New, Sentiment, Tagger
from datetime import date
import ast
from news_site import settings



class SentimentAnalysis:
    def __init__(self):
        self.util_path = settings.BASE_DIR
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
                temp_list.append((word))
            seperated_word_list.append(temp_list)
            a = tagger(news=query_set[i], split=temp_list)
            a.save()
            i += 1
        return seperated_word_list

    def get_score(self, query_set):
        sentiment_dict = pd.read_excel(self.util_path + "/sentiment_dictionary.xlsx")
        word_list = list(sentiment_dict['詞語'])
        sentiment_classifier = list(sentiment_dict['情感分類'])
        sentiment_score = list(sentiment_dict['強度'])
        i = 0
        for news in tqdm(query_set):
            news = news.split
            news = ast.literal_eval(news)
            #positive = 0
            #negative = 0
            anger = 0
            disgust = 0
            fear = 0
            sad = 0
            surprise = 0
            good = 0
            happy = 0
            for word in news:
                if word in word_list:
                    index = word_list.index(word)
                    if sentiment_classifier[index] in ['PA', 'PE']:
                        happy += sentiment_score[index]
                    if sentiment_classifier[index] in ['PD', 'PH', 'PG', 'PB', 'PK']:
                        good += sentiment_score[index]
                    if sentiment_classifier[index] in ['PC']:
                        surprise += sentiment_score[index]
                    if sentiment_classifier[index] in ['NAG']:
                        anger += sentiment_score[index]
                    if sentiment_classifier[index] in ['NB', 'NJ', 'NH', 'PF']:
                        sad += sentiment_score[index]
                    if sentiment_classifier[index] in ['NI', 'NC', 'NG']:
                        fear += sentiment_score[index]
                    if sentiment_classifier[index] in ['NE', 'ND', 'NN', 'NK', 'NL']:
                        disgust += sentiment_score[index]

            #positive_list.append(positive/len(news))
            #negative_list.append(negative/len(news))

            a = Sentiment(news=query_set[i].news, date=query_set[i].date, happy=happy,
                          good=good, surprise=surprise,
                          anger=anger, sad=sad,
                          fear=fear, disgust=disgust, length=len(news))
            a.save()
            i += 1

        return True