from rest_framework import routers
from django.urls import path
from .views import test_ltn_crawling, test_SETN_craling, test_EBC_craling, test_Asahi_craling, test_TVBS_craling, test_Upmedia_craling



urlpatterns = [
    path('api/ltn/', test_ltn_crawling, name='test ltn'),
    path('api/Asahi/', test_Asahi_craling, name='test Asahi'),
    path('api/EBC/', test_EBC_craling, name='test EBC'),
    path('api/TVBS/', test_TVBS_craling, name='test TVBS'),
    path('api/upmedia/', test_Upmedia_craling, name='test upmedia'),
]