from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Cart(object):

    def __init__(self, request):
        """Инициализируем корзину"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #  Сохраняю пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        """Добавить товар в корзину или обновить его количество"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии Cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """Удаление товара с корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных."""
        product_ids = self.cart.keys()
        # получение обьектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчет всех товаров"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        '''Подсчет стоимости товаров в корзине'''
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Удаление корзины из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / int('100')) * self.get_total_price()
        return int('0')

    def get_total_price_after_discount(self):
        return int(self.get_total_price() - self.get_discount())
