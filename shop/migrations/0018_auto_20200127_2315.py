# Generated by Django 2.2.6 on 2020-01-27 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20200127_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=1, max_length=100),
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='text',
            field=models.TextField(max_length=500, verbose_name='Характеристики'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
