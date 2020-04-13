import os
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from parler.models import TranslatableModel, TranslatedFields

# def get_image_path(instance, filename):
# 	return os.path.join('photos', str(instance.id), filename)

class Product(models.Model):
	"""Товар публикуемый на сайте"""
	# image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	title = models.CharField(max_length=100, verbose_name='Название')
	slug = models.SlugField(max_length=100, db_index=True)
	price = models.IntegerField(verbose_name='Цена')
	availability = models.BooleanField(default=True, verbose_name='Наличие')
	date_added = models.DateTimeField(auto_now_add=True, verbose_name='Был добавлен')
	updated = models.DateTimeField(auto_now=True, verbose_name='Был изменен')
	brand = models.ForeignKey('Brand', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Производитель')
	image_1 = models.ImageField(upload_to='images/', null=True, blank=True,)
	image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
	image_3 = models.ImageField(upload_to='images/', null=True, blank=True)
	rubric = models.ForeignKey('Rubric', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Рубрика')
	favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
	discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, verbose_name='Скидка (%)')

	class Meta:
		verbose_name_plural = 'Товар'
		verbose_name = 'Товар'
		ordering = ['price']

	def __str__(self):
		return f'{self.brand} {self.title}'

	def get_absolute_url(self):
		return reverse('shop:product', args=[self.brand.slug, self.slug])

	def get_discount(self):
		if self.discount:
			return (self.discount / int('100')) * self.price
		return int('0')

	def get_price(self):
		return int(self.price - self.get_discount())

	def get_bonuses(self):
		return int(self.get_price() / 20)

class Brand(models.Model):
	"""Производитель"""
	name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
	logo = models.ImageField(upload_to='images/brand/', null=True, blank=False)
	slug = models.SlugField(max_length=20, db_index=True, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Производители'
		verbose_name = 'Производитель'
		ordering = ['name']

class Rubric(TranslatableModel):
	"""Рубрика товара"""
	translations = TranslatedFields(
		name = models.CharField(max_length=50, db_index=True),
		slug = models.SlugField(max_length=50, db_index=True, unique=True)
	)

	# name = models.CharField(max_length=50, verbose_name='Название')
	# slug = models.SlugField(max_length=50, db_index=True, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['id']
		verbose_name_plural = 'Рубрики'
		verbose_name = 'Рубрика'

class Comment(models.Model):
	"""Отзывы пользователей"""
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80, verbose_name='имя', default='')
	email = models.EmailField(null=True)
	body = models.TextField(max_length=300, verbose_name='содержимое', default='')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Был добавлен')
	updated = models.DateTimeField(auto_now=True, verbose_name='Был изменен')
	is_active = models.BooleanField(default=True)
	value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

	class Meta:
		ordering = ['created']
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'

	def __str__(self):
		return f'Comment by {self.name}'

class Contact(models.Model):
	name = models.CharField(max_length=80, verbose_name='имя', blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	body = models.TextField(max_length=300, verbose_name='содержимое')
	image = models.ImageField(upload_to='contacts/', null=True, blank=True, verbose_name='скриншот')
	created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

	class Meta:
		ordering = ['created']
		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'

	def __str__(self):
		return f'{self.body[:30]}...'
