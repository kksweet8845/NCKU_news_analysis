from django.shortcuts import render
from django.http import HttpResponse
from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling, ftvnews_crawling
from newsdb.models import Subject, Brand, Brand_sub, New
from multiprocessing import Pool
from newsdb.serializers import NewSerializer
from datetime import datetime, date
from news_site import settings
import pickle
import json
import pandas as pd



def news_recrawling():
    n = New.objects.filter(content__exact="")
    for i in n:
        i.delete()
    # check
    n = New.objects.filter(content__exact="")
    print(len(n))

def database_clean():
    pass



def run():
    news_recrawling()