from django.db import models

class Product(models.Model):
	"""Товар публикуемый на сайте"""
	title = models.CharField(max_length=50, verbose_name='Название')
	text = models.TextField(max_length=400, verbose_name='Характеристики')
	price = models.IntegerField(verbose_name='Цена')
	availability = models.BooleanField(default=True, verbose_name='Наличие')
	date_added = models.DateTimeField(auto_now_add=True, verbose_name='Был добавлен')

	class Meta:
		verbose_name_plural = 'Товар' 
		verbose_name = 'Товар'
		ordering = ['price']
