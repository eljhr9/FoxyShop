from shop.models import Product
from django.conf import settings


class Compare(object):
    """Сессия сравнения товара"""
    def __init__(self, request):
        """Инициализируем корзину"""
        self.session = request.session
        compare = self.session.get(settings.COMPARE_SESSION_ID)
        if not compare:
            #  Сохраняю пустую корзину в сессии
            compare = self.session[settings.COMPARE_SESSION_ID] = {}
        self.compare = compare

    def add(self, product):
        """Добавить товар в корзину или обновить его количество"""
        product_id = str(product.id)
        if product_id not in self.compare:
            self.compare[product_id] = {'quantity': 1, 'price': str(product.price)}
        self.save()

    def save(self):
        # Обновление сессии compare
        self.session[settings.COMPARE_SESSION_ID] = self.compare
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """Удаление товара с корзины"""
        product_id = str(product.id)
        if product_id in self.compare:
            del self.compare[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных."""
        product_ids = self.compare.keys()
        # получение обьектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.compare[str(product.id)]['product'] = product

        for item in self.compare.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчет всех товаров"""
        return sum(item['quantity'] for item in self.compare.values())


    def clear(self):
        """Удаление корзины из сессии"""
        del self.session[settings.COMPARE_SESSION_ID]
        self.session.modified = True

    def availability(self, product):
        product_id = str(product.id)
        if product_id in self.compare:
            return True
        else:
            return False
