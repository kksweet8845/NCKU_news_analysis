from django.shortcuts import render
from django.http import HttpResponse
from .api import ltn_crawling
from newsdb.models import Subject, Brand, Brand_sub
# Create your views here.

def test_ltn_crawling(request):
    c = ltn_crawling()
    data = c.getNews(date='all')
    result = c.insertNews(data)
    return HttpResponse(data)
