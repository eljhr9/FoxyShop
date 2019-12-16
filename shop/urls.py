from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
	path('', views.products, name='products'),
	path('brand/<int:brand_id>/', views.by_brand, name='by_brand'),
	path('brand/', views.brand, name='brand'),
	path('<int:product_id>/', views.product, name='product'),
]
