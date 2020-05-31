import os
import pandas as pd
import numpy as np
import tensorflow.compat.v2 as tf
try:
    from tensorflow_text import SentencepieceTokenizer
    import tensorflow_hub as hub
except ModuleNotFoundError:
    pass
import sklearn.metrics.pairwise
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from django.db.models import Q
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
        dbscan = DBSCAN(eps=0.4*np.log(len(similarity))-1.15, min_samples=2).fit_predict(1-similarity)
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