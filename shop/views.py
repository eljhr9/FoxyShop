from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Product, Brand

def index(request):
	'''домашняя страница магазина'''
	return render(request, 'shop/index.html')


def products(request):
	'''Отображение всех товаров'''
	products = Product.objects.all()
	brands = Brand.objects.all()
	context = {'products': products, 'brands': brands}
	return render(request, 'shop/products.html', context)

def brand(request):
	brands = Brand.objects.all()
	context = {'brands': brands}
	return render(request, 'shop/brand.html', context)

def by_brand(request, brand_id):
	products = Product.objects.filter(brand=brand_id)
	brands = Brand.objects.all()
	current_brand = Brand.objects.get(pk=brand_id)
	context = {'products': products, 'brands': brands, 'current_brand': current_brand}
	return render(request, 'shop/by_brand.html', context)
