from rest_framework import routers
from django.urls import path
from .views import test_ltn_crawling



urlpatterns = [
    path('api/ltn/', test_ltn_crawling, name='test ltn')
]