from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователи')
    phone_number = models.CharField(max_length=10, null=True, blank=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватарка')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['user']

    def __str__(self):
        return f'{self.user} профиль'

class Bonuses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователи')
    summa = models.IntegerField(verbose_name='Колличество')
    description = models.CharField(max_length=150, verbose_name='Описание')
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Бонусы'
        verbose_name_plural = 'Бонусы'
        ordering = ['date']
