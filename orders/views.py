from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def create_order(request):
    cart = Cart(request)
    if request.method == "POST" and ('order_form' in request.POST or 'order_form_payment' in request.POST):
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            cart.clear()
            orderitems = OrderItem.objects.filter(order=order)
            if 'order_form_payment' in request.POST:
                request.session['order_id'] = order.id
                return redirect(reverse('payment:process'))
            else:
                order_url = request.build_absolute_uri(order.get_absolute_url())
                order_created.delay(order.id, order_url)
                return render(request, 'orders/created.html', {'order': order, 'orderitems': orderitems})

    else:
        order_form = OrderCreateForm()
    context = {'cart': cart, 'order_form': order_form}
    return render(request, 'orders/create.html', context)

def order_test(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order)
    return render(request, 'orders/created.html', {'order': order, 'orderitems': orderitems})
