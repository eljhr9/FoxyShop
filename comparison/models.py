from django.db import models
from shop.models import Product


class Characteristic(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='characteristic', verbose_name='Товар')
    diagonal = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='Диагональ (дюйм)')
    display_type = models.CharField(max_length=10, null=True, blank=True, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=10, null=True, blank=True, verbose_name='Разрешение (пикс)')
    processor = models.CharField(max_length=20, null=True, blank=True, verbose_name='Процессор')
    ram = models.IntegerField(null=True, blank=True, verbose_name='Оперативная память')
    storage = models.IntegerField(null=True, blank=True, verbose_name='Встроеная память (Гб)')
    year = models.IntegerField(null=True, blank=True, verbose_name='Год выпуска')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ['product']

    def __str__(self):
        return f'{self.product}'
