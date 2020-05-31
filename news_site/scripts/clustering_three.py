import os
import pandas as pd
import numpy as np
import tensorflow.compat.v2 as tf
from tensorflow_text import SentencepieceTokenizer
import tensorflow_hub as hub
import sklearn.metrics.pairwise
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from django.db.models import Q
from newsdb.models import New, cluster_day, cluster_three_days
from datetime import date, timedelta
from tqdm import tqdm


class NewsClustering:
    def __init__(self):
        pass

    def getModel(self):
        model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual/3')
        return model

    def embed_text(self, model, text):
        return model(text)

    def cos_sim(self, input_vectors):
        similarity = cosine_similarity(input_vectors)
        return similarity
    
    def remove_covid_message(self, content):
        a = '看更多 武漢肺炎（COVID-19、新冠肺炎）疫情'
        b = 'if(!detectmob()&&'
        head, sep, tail = content.partition(a)
        head, sep, tail = head.partition(b)
        return head

    def getNewsCluster(self, similarity):
        cluster_list = []
        dbscan = DBSCAN(eps=max(0.5, 0.4*np.log(len(similarity))-1.5), min_samples=2).fit_predict(1-similarity)
        for i in range(len(similarity)):
            temp = []
            for j in range(len(similarity)):
                if dbscan[j] == i:
                    temp.append(j)
            if temp:        
                cluster_list.append(temp)
        return cluster_list

    def getTopNewsIndex(self, cluster_list):
        return cluster_list
        

    def getEmbed(self, query_set):
        model = self.getModel()
        news_list = []
        for query in query_set:
            content = query.content
            content = self.remove_covid_message(content)
            news_list.append(content)
        news = self.embed_text(model, news_list)
        return news


    def getTopNews(self, news):
        similarity = self.cos_sim(news)
        cluster_list = self.getNewsCluster(similarity)
        top_news = self.getTopNewsIndex(cluster_list)
        return top_news

def run():
    news_clustering = NewsClustering()

    for j in range(17):
        news_query = New.objects.filter(Q(date__gt=((date.today()-timedelta(days=3)).isoformat()) & Q(brand=j+1)))
        text = tf.Variable(np.empty((0,512)), dtype=np.float32)
        for i in tqdm(range(int(len(news_query)/100) + 1)):
            temp = news_clustering.getEmbed(news_query[(i*100):((i+1)*100)])
            text = tf.concat((text, temp), axis=0)
        top_news = news_clustering.getTopNews(text)
        top_news.sort(key=len, reverse=True)

        cluster_no = 1
        for news_list in tqdm(top_news):
            for news in news_list:
                a = cluster_three_days(news=news_query[news], date=news_query[news].date, cluster=cluster_no, date_today=date.today().isoformat)
                a.save()
            cluster_no += 1
