from django.urls import path
from . import views

urlpatterns = [
    # testing path
    path('hotword', views.hotword),
    path('wordmap', views.wordmap),
    path('keyword', views.keyword),
    path('pubKeyword', views.pubKeyword),
    path('dumpNews', views.dumpArticle),
    path('wordFreq', views.wordFreq),
    path('memory', views.newsMemory),
    path('sentiment', views.get_sentiment),
    path('standpoint', views.get_standpoint),
    path('cluster', views.get_cluster),
    # official path
    path('sentimentWeek', views.sentimentWeek),
    path('newsReview', views.newsReview),
    path('top20Keywords', views.top20Keywords),
    path('mediaReport', views.mediaReport),
    path('keywordAnalysis/<str:word>', views.keywordAnalysis),
    path('relativeKeyword/<str:word>', views.relativeKeyword),
    path('mediaAnalysis', views.mediaAnalysis),
]