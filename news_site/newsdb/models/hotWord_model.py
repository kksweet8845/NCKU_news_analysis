from django.db import models
from .subjects_model import Subject
from .brands_model import Brand
from .wordsMap_model import Word


class HotWord(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    tally = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0
    )

    def __str__(self):
        return "{}\n{}\n{}\n{}\n{}".format(self.word, self.brand, self.sub, self.date, self.tally)
    class Meta:
        db_table = "hot_words"