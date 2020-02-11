from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


def create_order(request):
    cart = Cart(request)
    if request.method == "POST" and 'order_form' in request.POST:
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})
    else:
        order_form = OrderCreateForm()
    context = {'cart': cart, 'order_form': order_form}
    return render(request, 'orders/create.html', context)


def order_test(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order)
    return render(request, 'orders/created.html', {'order': order, 'orderitems': orderitems})
