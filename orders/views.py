from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from users.models import Bonuses


def create_order(request):
    cart = Cart(request)
    if request.method == "POST" and ('order_form' in request.POST or 'order_form_payment' in request.POST):
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            request.session['coupon_id'] = None
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            cart.clear()
            orderitems = OrderItem.objects.filter(order=order)
            order_url = request.build_absolute_uri(order.get_absolute_url())
            order_created.delay(order.id, order_url)
            if request.user.is_authenticated:
                description = f'Оформление заказа №{order.id}'
                Bonuses.objects.create(user=request.user, summa=order.get_bonuses_summ(), description=description)
            if 'order_form_payment' in request.POST:
                request.session['order_id'] = order.id
                return redirect(reverse('payment:process'))
            else:
                return render(request, 'orders/created.html', {'order': order, 'orderitems': orderitems})

    else:
        if request.user.is_authenticated:
            order_form = OrderCreateForm(instance=request.user)
        else:
            order_form = OrderCreateForm()
    context = {'cart': cart, 'order_form': order_form}
    return render(request, 'orders/create.html', context)

def order_test(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order)
    return render(request, 'orders/created.html', {'order': order, 'orderitems': orderitems})
