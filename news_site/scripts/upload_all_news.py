from django.shortcuts import render
from django.http import HttpResponse
from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling, ftvnews_crawling
# from crawling.apis import CNACrawler, EBCCrawler, NewtalkCrawler, SETNCrawler, TVBSCrawler, UpmediaCrawler, StormCrawler, ChinatimesCrawler
from newsdb.models import Subject, Brand, Brand_sub
from multiprocessing import Pool
from newsdb.serializers import NewSerializer
from datetime import datetime, date
from news_site import settings
import pickle
import json
import pandas as pd
from analysis.apis import AspectModule
from newsdb.models import New
from django.db.models import Q


# def get_news_today(request):
#     apis = [
#         SETNCrawler,
#         CNACrawler,
#         EBCCrawler,
#         NewtalkCrawler,
#         TVBSCrawler,
#         UpmediaCrawler,
#         StormCrawler,
#         ChinatimesCrawler,
#     ]

#     for api in apis:
#         try:
#             crawler = api()
#             news_today = crawler.get_news_today()
#             #news_today = crawler.get_news_by_date(date_list=["2020-05-24", "2020-05-25", "2020-05-26", "2020-05-27", "2020-05-28", "2020-05-29"])
#             result = crawler.insert_news(news_today)

#             print('successful')
#         except Exception as e:
#             print(e)
#             print('error in crawler')
#             continue

#     return HttpResponse(True)


def todayNews_crawling(request):
    ls = [
        ('cts', cts_crawling()),
        ('ltn',ltn_crawling()),
        ('nowNews', nowNews_crawling()),
        ('udn', udn_crawling()),
        ('ftvnews', ftvnews_crawling()),
        ('pts', pts_crawling()),
    ]
    errors = []
    df = pd.DataFrame(columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url'])
    for name, i in ls:
        print("="*150)
        new_data = []
        data = i.getNews(date=['2020-05-30', '2020-05-28', '2020-05-07', '2020-05-06','2020-05-05', '2020-05-04','2020-05-03', '2020-05-02', '2020-05-01', '2020-04-28', '2020-04-29', '2020-04-30'])
        for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
                new_data.append(j)
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
        print(len(new_data))
        result = i.insertNews(new_data)
        if result != None:
            result = pd.DataFrame([ dr.__dict__ for dr in result],
                              columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url'])
            df.append(result)
        print(f"{name} finished")
    with open(f'{settings.BASE_DIR}/../error/{date.today().isoformat()}_error.json',"w+") as file:
        file.write(json.dumps(errors))
    return df


def analysis_aspect(df):
    util_path = settings.BASE_DIR + '/analysis/apis/utils/aspect_data/chineseGLUE/inews/'


    # save the current file into csv
    df \
        .drop('author',axis=1,inplace=True) \
        .drop('date',axis=1,inplace=True) \
        .drop('update_time', axis=1, inplace=True) \
        .drop('brand_id', axis=1,inplace=True) \
        .drop('sub_id', axis=1, inplace=True) \
        .drop('url', axis=1, inplace=True)
    df = df[['title', 'content', 'id']]
    df.to_csv(util_path + 'eval_tc.csv')

    aspectModule = AspectModule('eval')
    result, acc = aspectModule.eval('bert-base-chinese-e-3.ckpt')
    print(result, acc)


def run():
    # Crawling the news
    # get_news_today(None)
    todayNews_crawling(None)
    # tagger
