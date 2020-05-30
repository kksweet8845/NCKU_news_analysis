# Generated by Django 3.0.3 on 2020-05-24 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsdb', '0011_auto_20200524_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentiment',
            name='anger',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sentiment',
            name='disgust',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sentiment',
            name='fear',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sentiment',
            name='good',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sentiment',
            name='happy',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sentiment',
            name='sad',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sentiment',
            name='surprise',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
