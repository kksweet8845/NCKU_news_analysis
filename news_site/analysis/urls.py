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
    path('cluster', views.get_cluster)
]