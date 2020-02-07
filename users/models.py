from django.db import models
from django.conf import settings
# from django.contrib.auth.models import AbstractUser
#
#
# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)

# class MyUser(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#
# USERNAME_FIELD = 'email'

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
