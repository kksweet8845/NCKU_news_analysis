from django.urls import path
from . import views

urlpatterns = [
    path('hotword', views.hotword),
    path('wordmap', views.wordmap),
    path('keyword', views.keyword),
    path('pubKeyword', views.pubKeyword),
    path('dumpNews', views.dumpArticle),
    path('wordFreq', views.wordFreq)
]