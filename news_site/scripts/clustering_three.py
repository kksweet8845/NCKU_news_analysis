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
from newsdb.models import New, Cluster_day, Cluster_three_day
from datetime import date, timedelta
from tqdm import tqdm
from analysis.apis import NewsClustering



def run():
    news_clustering = NewsClustering()

    for j in range(17):
        news_query = New.objects.filter(Q(date__gt=((date.today()-timedelta(days=3)).isoformat())) & Q(brand=j+1))
        if len(news_query) == 0:
            continue
        text = tf.Variable(np.empty((0,512)), dtype=np.float32)
        for i in tqdm(range(int(len(news_query)/100) + 1)):
            temp = news_clustering.getEmbed(news_query[(i*100):((i+1)*100)])
            text = tf.concat((text, temp), axis=0)
        top_news = news_clustering.getTopNews(text)
        top_news.sort(key=len, reverse=True)

        cluster_no = 1
        for news_list in tqdm(top_news):
            for news in news_list:
                a = Cluster_three_day(news=news_query[news], date=news_query[news].date, cluster=cluster_no, date_today=date.today().isoformat())
                a.save()
            cluster_no += 1
