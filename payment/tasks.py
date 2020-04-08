from celery import task
from django.core.mail import send_mail
from orders.models import Order, OrderItem
from django.template.loader import render_to_string


@task
def order_payed(order_id, order_url):
	"""
	Task to send an e-mail notification when an order is successfully payed.
	"""
	order = Order.objects.get(id=order_id)
	orderitems = OrderItem.objects.filter(order=order)
	subject = f'Оплата заказа в магазине "FoxyShop" номер {order.id}'
	message = f'Dear {order.first_name},\n\nYou have successfully placed an order.\
				Your order id is {order.id}.'
	html = render_to_string('order_payed.html', {'order': order, 'orderitems': orderitems, 'order_url': order_url})
	mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email],  html_message=html)
	return mail_sent
