from django import template

register = template.Library()

from ..models import Product, Comment
from django.db.models import Avg
from comparison.comparison import Compare


@register.simple_tag
def total_posts(product_id=1):
    product = Product.objects.get(id=product_id)
    a = 0
    b = product.comments.count()
    if b == 0:
        b = 1
    for comment in Comment.objects.filter(product=product):
        a += comment.value
    if a == 0:
        a = 1
    a = a / b
    return int(a)

# @register.inclusion_tag('shop/avg_value.html')
# @register.simple_tag
# def show_avg_value(product_id):
#     product = Product.objects.get(id=product_id)
#     review_value = Comment.objects.filter(product=product).aggregate(Avg('value'))
#     return {'review_value': review_value}
