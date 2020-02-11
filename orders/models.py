from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=25, verbose_name='Ваше имя')
    last_name = models.CharField(max_length=25, null=True, blank=True, verbose_name='Фамилия')
    email = models.EmailField()
    phone = models.CharField(max_length=13, null=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=200, verbose_name='Адресс')
    postal_code = models.CharField(max_length=10, verbose_name='Почтовый индекс')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.DO_NOTHING, verbose_name='Товар')
    price = models.IntegerField(verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
