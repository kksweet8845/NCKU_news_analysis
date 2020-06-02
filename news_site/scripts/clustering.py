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
from newsdb.models import New, Cluster_day
from datetime import date, timedelta, datetime
from tqdm import tqdm
from analysis.apis import NewsClustering


def zero(num):
    return f"0{num}" if num < 10 else f"{num}"

def run():
    news_clustering = NewsClustering()
    # base = datetime(2020,5,)
    # date_list = [ base - timedelta(days=x) for x in range(7)]
    # date_list = [ f'{dd.year}-{zero(dd.month)}-{zero(dd.day)}' for dd in date_list]
    date_list = ['2020-06-01', '2020-06-02', '2020-05-31']
    for dd in date_list:
        news_query = New.objects.filter(Q(date=dd))
        if len(news_query) == 0:
            continue
        text = tf.Variable(np.empty((0,512)), dtype=np.float32)
        for i in tqdm(range(int(len(news_query)/100) + 1)):
            temp = news_clustering.getEmbed(news_query[(i*100):((i+1)*100)])
            text = tf.concat((text, temp), axis=0)
        top_news = news_clustering.getTopNews(text)
        top_news.sort(key=len, reverse=True)

        # print(top_news)
        cluster_no = 1
        for news_list in tqdm(top_news):
            for news in news_list:
                a = Cluster_day(news=news_query[news], date=news_query[news].date, cluster=cluster_no)
                a.save()
            cluster_no += 1
