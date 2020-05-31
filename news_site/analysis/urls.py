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
<<<<<<< HEAD
    path('top20Keywords', views.testChoose),
    path('relativeKeyword/<str:word>', views.testRelativeKeyword),
    path('keywordAnalysis/<str:word>', views.testKeywordAnalysis),
    path('sentimentWeek', views.testSevenSemantic),
    path('newsAnalysis', views.testReview)
=======
    path('cluster', views.get_cluster),
    # official path
    path('sentimentWeek', views.sentimentWeek),
    path('newsReview', views.newsReview),
    path('top20Keywords', views.top20Keywords),
    path('mediaReport', views.mediaReport),
    path('keywordAnalysis/<str:word>', views.keywordAnalysis),
    path('relativeKeyword/<str:word>', views.relativeKeyword),
    path('mediaAnalysis', views.mediaAnalysis),
>>>>>>> bcf883ef0788d70ac9d77a9a463b0c8557fbfaf5
]