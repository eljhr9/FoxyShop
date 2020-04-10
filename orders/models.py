from django.db import models
from shop.models import Product
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(max_length=25, verbose_name=_('Ваше имя'))
    last_name = models.CharField(max_length=25, null=True, blank=True, verbose_name=_('Фамилия'))
    email = models.EmailField(_('email'))
    phone = models.CharField(max_length=13, null=True, verbose_name=_('Номер телефона'))
    city = models.CharField(max_length=100, verbose_name=_('Город'))
    address = models.CharField(max_length=200, verbose_name=_('Адресс'))
    postal_code = models.CharField(max_length=10, verbose_name=_('Почтовый индекс'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Изменен'))
    paid = models.BooleanField(default=False, verbose_name=_('Оплачено'))
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Купон'))
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('Скидка'))

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    def __str__(self):
        return f'{self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return int(total_cost - total_cost * (self.discount / int('100')))

    def get_absolute_url(self):
    		return reverse('orders:order', args=[self.id])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_('Заказ'))
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.DO_NOTHING, verbose_name=_('Товар'))
    price = models.IntegerField(verbose_name=_('Цена'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Количество'))

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
