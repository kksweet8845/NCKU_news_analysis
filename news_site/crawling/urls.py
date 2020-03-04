from rest_framework import routers
from django.urls import path
from .views import test_ltn_crawling, test_SETN_craling, test_EBC_craling, test_Aljazeera_craling



urlpatterns = [
    path('api/ltn/', test_ltn_crawling, name='test ltn'),
    path('api/SETN/', test_SETN_craling, name='test SETN'),
    path('api/EBC/', test_EBC_craling, name='test EBC'),
    path('api/Aljazeera/', test_Aljazeera_craling, name='test Aljazeera'),
]