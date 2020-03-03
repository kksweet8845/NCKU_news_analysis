# local Django
from django.db import models


class BrandForeign(models.Model):
    brand_name = models.CharField(
        max_length=20,
        blank=False,
        default=''
    )
    href = models.CharField(
        max_length=1000,
        blank=False,
        default=''
    )

    def __str__(self):
        return "brand_name: {}".format(self.brand_name)

    class Meta:
        db_table = "brands_foreign"