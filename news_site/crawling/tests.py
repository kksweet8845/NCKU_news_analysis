from django.test import TestCase
from api import ltn_crawling
from rest_framework.response import Response
# Create your tests here.

def test_ltn_crawling(request):
    c = ltn_crawling()
    data = c.crawl_category()