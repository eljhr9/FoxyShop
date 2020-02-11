from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
	path('all/', views.products, name='products'),
	path('search/', views.product_search, name='product_search'),
	path('brand/<slug:brand_slug>/', views.by_brand, name='by_brand'),
	path('brand/', views.brand, name='brand'),
	path('<slug:brand_slug>/<slug:product_slug>/', views.product, name='product'),
	path('<slug:rubric_slug>/', views.products, name='by_rubric'),
]
