from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm, OrderDeliveryForm
from cart.cart import Cart
from .tasks import order_created
from users.models import Bonuses, Delivery


def create_order(request):
    cart = Cart(request)
    if request.method == "POST" and ('order_form' in request.POST or 'order_form_payment' in request.POST):
        order_form = OrderCreateForm(request.POST)
        order_delivery = OrderDeliveryForm(request.POST)
        if order_form.is_valid() and order_delivery.is_valid():
            order = order_form.save(commit=False)
            cd = order_delivery.cleaned_data
            order.city = cd['city']
            order.address = cd['address']
            order.postal_code = cd['postal_code']
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
            delivery = Delivery.objects.filter(user=request.user)
            if not delivery:
                delivery = Delivery.objects.create(user=request.user)
            order_delivery = OrderDeliveryForm(instance=delivery)
        else:
            order_form = OrderCreateForm()
            order_delivery = OrderDeliveryForm()
    context = {'cart': cart, 'order_form': order_form, 'order_delivery': order_delivery}
    return render(request, 'orders/create.html', context)

def order_test(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order)
    return render(request, 'orders/created.html', {'order': order, 'orderitems': orderitems})
