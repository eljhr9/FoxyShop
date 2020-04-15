from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if 'quantity' in request.POST:
            cart.add(product=product, update_quantity=True, quantity=cd['quantity'])
        elif 'quantity+' in request.POST:
            cart.add(product=product, update_quantity=True, quantity=cd['quantity']+1)
        else:
            cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    if 'products' in request.POST:
        return redirect('shop:products')
    elif 'product' in request.POST:
        return redirect(product.get_absolute_url())
    elif 'quick_checkout' in request.POST:
        return redirect('orders:create_order')
    else:
        return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
