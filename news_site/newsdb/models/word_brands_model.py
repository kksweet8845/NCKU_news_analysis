from django.db import models
from .brands_model import Brand
from .subjects_model import Subject
from .wordsMap_model import Word

class Word_brand(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    ner_flag = models.BooleanField(
        default=False
    )
    ner = models.CharField(
        max_length=20,
    )

    def __str__(self):
        return "{}\n{}\n{}\n{} {}".format(self.brand, self.sub,self.word, self.ner_flag, self.ner)

    class Meta:
        db_table = "word_brands"