from rest_framework import routers
from django.urls import path
from .views import test_ltn_crawling, test_nowNews_crawling, test_pts_crawling, test_udn_crawling, test_cts_crawling, test_ftvnews_crawling
from .views import todayNews_crawling


urlpatterns = [
    path('api/ltn/', test_ltn_crawling, name='test ltn'),
    path('api/nowNews/', test_nowNews_crawling, name='test nowNews'),
    path('api/pts/', test_pts_crawling, name='test pts'),
    path('api/udn/', test_udn_crawling, name='test udn'),
    path('api/cts/', test_cts_crawling, name='test cts'),
    path('api/ftvnews/', test_ftvnews_crawling, name='test ftvnews'),
    path('api/newsToday/', todayNews_crawling, name='crawl todayNews')
]