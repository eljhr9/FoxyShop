from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Значение')
    valid_from = models.DateTimeField(verbose_name='Действительный с')
    valid_to = models.DateTimeField(verbose_name='Действительный до')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка (%)')
    active = models.BooleanField()

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code
