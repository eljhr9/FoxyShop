from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('test/<int:order_id>/', views.order_test , name='order_test')
]
