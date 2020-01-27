from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
	path('all/', views.products, name='products'),
	path('brand/<slug:brand_slug>/', views.by_brand, name='by_brand'),
	path('brand/', views.brand, name='brand'),
	path('<int:product_id>/', views.product, name='product'),
	path('<slug:rubric_slug>/', views.by_rubric, name='by_rubric'),
]
