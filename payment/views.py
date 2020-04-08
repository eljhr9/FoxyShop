import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order, OrderItem
from .tasks import order_payed


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale({
			'amount': '{:.2f}'.format(order.get_total_cost()),
			'payment_method_nonce': nonce,
			'options': {
				'submit_for_settlement': True
			}
		})
        order_url = request.build_absolute_uri(order.get_absolute_url())
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            order_payed.delay(order.id, order_url)
            return render(request, 'orders/created.html', {'order': order, 'orderitems': orderitems})
        else:
            return redirect('payment:canceled')
    else:
        client_token = braintree.ClientToken.generate()
        context = {'order': order, 'client_token': client_token}
        return render(request, 'payment/process.html', context)

def payment_done(request):
	return render(request, 'payment/done.html')

def payment_canceled(request):
	return render(request, 'payment/canceled.html')
