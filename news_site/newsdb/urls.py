from rest_framework import routers
from .api import NewViewSet, Brand_subViewSet, BrandViewSet, SubjectViewSet


router = routers.DefaultRouter()
router.register('api/news', NewViewSet, 'newsdb-news')
router.register('api/brand_sub', Brand_subViewSet, 'newsdb-brand_sub')
router.register('api/brand', BrandViewSet, 'newsdb-brand')
router.register('api/subject', SubjectViewSet, 'newsdb-subject')
urlpatterns = router.urls