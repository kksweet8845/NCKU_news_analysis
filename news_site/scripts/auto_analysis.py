from django.shortcuts import render
from django.http import HttpResponse
from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling, ftvnews_crawling
from newsdb.models import Subject, Brand, Brand_sub, New, Aspect
from multiprocessing import Pool
from newsdb.serializers import NewSerializer
from datetime import datetime, date
from news_site import settings
import pickle
import json, re
import pandas as pd
from analysis.apis import AspectModule
from newsdb.models import New
from django.db.models import Q


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
    df = pd.DataFrame(columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url'])
    for name, i in ls:
        print("="*150)
        new_data = []
        # data = i.getNews(date=['2020-05-18', '2020-05-19'])
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
        result = pd.DataFrame(result,
                              columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url'])
        df.append(result)
        print(f"{name} finished")
    with open(f'{settings.BASE_DIR}/../error/{date.today().isoformat()}_error.json',"w+") as file:
        file.write(json.dumps(errors))
    return df


def analysis_aspect(df):
    util_path = settings.BASE_DIR + '/analysis/apis/utils/aspect_data/chineseGLUE/inews/'


    print(df.head())
    # save the current file into csv
    df.drop('author',axis=1,inplace=True)
    df.drop('date',axis=1,inplace=True)
    df.drop('update_time', axis=1, inplace=True)
    df.drop('brand_id', axis=1,inplace=True)
    df.drop('sub_id', axis=1, inplace=True)
    df.drop('url', axis=1, inplace=True)
    df = df[['title', 'content', 'id']]

    def cleanP(row):
        content = row['content']
        tmp = re.sub(r'[\n]', ' ', content)
        row['content'] = tmp
        title = row['title']
        tmp = re.sub(r'[\n]', ' ', title)
        row['title'] = tmp
        return row
    # df = df.apply(cleanP, axis=1)
    # df.to_csv(util_path + 'eval_tc.csv')

    aspectModule = AspectModule(df, 'eval', 8)
    result = aspectModule.eval('bert-base-chinese-e-3.ckpt')

    all_news = New.objects.all()
    cur_asp = Aspect.objects.all()
    for dp, di in result:
        if len(cur_asp.filter(new_id=di)) == 0:
            tmp = Aspect(**{'aspect': dp, 'new':all_news.get(id=di)})
            tmp.save()


    print(result)


def run():
    # Crawling the news
    # todayNews_crawling(None)
    # tagger
    news = New.objects.filter(*[Q(date__gte='2020-05-01'), Q(date__lte='2020-05-24')])

    df = pd.DataFrame(list(news.values()),
                      columns=[
                      'id',
                      'title',
                      'content',
                      'author',
                      'brand_id',
                      'sub_id',
                      'date',
                      'update_time',
                      'url']
    )
    print(df.head())
    analysis_aspect(df)
