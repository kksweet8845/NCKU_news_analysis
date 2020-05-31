from django.urls import path
from . import views

urlpatterns = [
    path('hotword', views.hotword),
    path('wordmap', views.wordmap),
    path('keyword', views.keyword),
    path('pubKeyword', views.pubKeyword),
    path('dumpNews', views.dumpArticle),
    path('wordFreq', views.wordFreq),
    path('sentiment', views.get_sentiment),
    path('standpoint', views.get_standpoint),
    path('top20Keywords', views.testChoose),
    path('relativeKeyword/<str:word>', views.testRelativeKeyword),
    path('keywordAnalysis/<str:word>', views.testKeywordAnalysis),
    path('sentimentWeek', views.testSevenSemantic),
    path('newsAnalysis', views.testReview)
]