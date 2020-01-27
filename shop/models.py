import os
from django.db import models
from django.urls import reverse

# def get_image_path(instance, filename):
# 	return os.path.join('photos', str(instance.id), filename)

class Product(models.Model):
	"""Товар публикуемый на сайте"""
	# image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	title = models.CharField(max_length=100, verbose_name='Название')
	slug = models.SlugField(max_length=100, db_index=True, default=1)
	text = models.TextField(max_length=500, verbose_name='Характеристики')
	price = models.IntegerField(verbose_name='Цена')
	availability = models.BooleanField(default=True, verbose_name='Наличие')
	date_added = models.DateTimeField(auto_now_add=True, verbose_name='Был добавлен')
	brand = models.ForeignKey('Brand', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Производитель')
	image_1 = models.ImageField(upload_to='images/', null=True, blank=True)
	image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
	image_3 = models.ImageField(upload_to='images/', null=True, blank=True)
	rubric = models.ForeignKey('Rubric', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Рубрика')

	class Meta:
		verbose_name_plural = 'Товар'
		verbose_name = 'Товар'
		ordering = ['price']

	def get_absolute_url(self):
		return reverse('shop:product', args=[self.brand.slug, self.slug])

class Brand(models.Model):
	"""Производитель"""
	name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
	logo = models.ImageField(upload_to='images/brand/', null=True, blank=True)
	slug = models.SlugField(max_length=20, db_index=True, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Производители'
		verbose_name = 'Производитель'
		ordering = ['name']

class Rubric(models.Model):
	name = models.CharField(max_length=50, verbose_name='Название')
	slug = models.SlugField(max_length=50, db_index=True, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['id']
		verbose_name_plural = 'Рубрики'
		verbose_name = 'Рубрика'

class Comment(models.Model):
	"""Отзывы пользователей"""
