# Generated by Django 3.0.2 on 2020-03-05 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsdb', '0004_new_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='author',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='new',
            name='content',
            field=models.CharField(default='', max_length=4000),
        ),
    ]
