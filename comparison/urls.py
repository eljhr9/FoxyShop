from django.urls import path
from . import views

app_name = 'compare'

urlpatterns = [
    path('', views.compare_detail, name='compare_detail'),
    path('add/<int:product_id>/', views.compare_add, name='compare_add'),
    path('remove/<int:product_id>/', views.compare_remove, name='compare_remove'),
]
