# local Django
from newsdb.models import BrandForeign

class DatabaseInit:
    def init_brand_foreign():
        brands = [{
            'id': 1,
            'brand_name': '半島中文網'
        }]