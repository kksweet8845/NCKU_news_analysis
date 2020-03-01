from django.db import models
from .subjects_model import Subject
from .brands_model import Brand

class Brand_sub(models.Model):
    # brand_id = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=0,
    #     blank=False
    # )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default='')
    # sub_id = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=0,
    #     blank=False
    # )
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE, default='')
    index_href = models.CharField(
        max_length=1000,
        blank=False,
        default=''
    )
    ajax_href = models.CharField(
        max_length=1000,
        blank=False,
        default=''
    )
    def __str__(self):
        return "{}\n{}\nindex_href: {}".format(self.brand, self.sub, self.index_href)
    class Meta:
        db_table = "brands_sub"
