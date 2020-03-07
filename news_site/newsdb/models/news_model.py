from django.db import models
from django.utils import timezone
from .brands_model import Brand
from .subjects_model import Subject

class New(models.Model):
    title   = models.CharField(
        max_length=200,
        blank=False,
        default=''
    )
    content = models.CharField(
        max_length=4000,
        blank=False,
        default=''
    )
    author  = models.CharField(
        max_length=50
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date    = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    update_time = models.DateTimeField(
        default=timezone.now
    )
    url = models.CharField(
        max_length=1000,
        default=''
    )
    def __str__(self):
        return ""
    class Meta:
        db_table = "news"