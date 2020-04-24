from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('keyword', views.keywordPage),
    path('publisher', views.publisherPage),
    path('foreign', views.foreignPage)
]