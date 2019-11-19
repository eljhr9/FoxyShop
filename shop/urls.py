from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
	path('', views.products, name='products'),
]