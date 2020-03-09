from rest_framework import routers
from django.urls import path
from .views import test_ltn_crawling, test_SETN_craling, test_EBC_craling, test_Asahi_craling, test_TVBS_craling, test_Upmedia_craling, test_Sputniknews_craling, test_JoongAng_craling, test_Huanqiu_craling
from .views import get_foregin_news_today


urlpatterns = [
    path('api/ltn/', test_ltn_crawling, name='test ltn'),
    path('api/Asahi/', test_Asahi_craling, name='test Asahi'),
    path('api/Sputniknews/', test_Sputniknews_craling, name='test sputniknews'),
    path('api/TVBS/', test_TVBS_craling, name='test TVBS'),
    path('api/upmedia/', test_Upmedia_craling, name='test upmedia'),
    path('api/JoongAng/', test_JoongAng_craling, name='test JoongAng'),
    path('api/Huanqiu/', test_Huanqiu_craling, name='test Huanqiu'),
    path('api/GetForeginNewsToday/', get_foregin_news_today, name='get foregin news today')
]