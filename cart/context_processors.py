from .cart import Cart
from shop.models import Product

def cart(request):
    cartitem = request.session.get('cart')
    try:
        cartitems = Product.objects.filter(id__in=cartitem)
    except:
        cartitems = None
    return {'cartitems': cartitems, 'cart': Cart(request)}
