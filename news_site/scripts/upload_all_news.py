from django.shortcuts import render
from django.http import HttpResponse
from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling, ftvnews_crawling
from newsdb.models import Subject, Brand, Brand_sub
from multiprocessing import Pool
from newsdb.serializers import NewSerializer
from datetime import datetime, date
from news_site import settings
import pickle
import json


def todayNews_crawling(request):
    ls = [
        ('ltn',ltn_crawling()),
        ('nowNews', nowNews_crawling()),
        ('udn', udn_crawling()),
        ('ftvnews', ftvnews_crawling()),
        ('pts', pts_crawling()),
        ('cts', cts_crawling())
    ]
    errors = []
    prev_data = None
    try:
        f = open("/tmp/news.obj", "rb")
        prev_data = pickle.load(f)
    except FileNotFoundError as err:
        pass
    for name, i in ls:
        print("="*150)
        new_data = []
        data = i.getNews(date=[date.today().isoformat()])
        for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
                new_data.append(j)
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
        result = i.insertNews(new_data)
        print(f"{name} finished")
    with open(f'{settings.BASE_DIR}/../error/{date.today().isoformat()}_error.json',"w+") as file:
        file.write(json.dumps(errors))

def run():
    # Crawling the news
    todayNews_crawling(None)
    # tagger

