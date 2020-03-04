# local Django
from django.db import models
from django.utils import timezone
from .brands_foreign_model import BrandForeign
from .subjects_model import Subject

class NewsForeign(models.Model):
    title   = models.CharField(
        max_length=200,
        blank=False,
        default=''
    )
    content = models.CharField(
        max_length=2000,
        blank=False,
        default=''
    )
    author  = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )
    brand = models.ForeignKey(
        BrandForeign, 
        on_delete=models.CASCADE
    )
    sub = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE
    )
    date    = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    update_time = models.DateTimeField(
        default=timezone.now
    )
    url  = models.CharField(
        max_length=1000
    )
    is_headline = models.BooleanField(
        default= False
    )

    class Meta:
        db_table = "news_foreign"
    
    def __str__(self):
        return ""