from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Product, Brand
from django.core.paginator import Paginator

def index(request):
	'''домашняя страница магазина'''
	brands = Brand.objects.all()
	return render(request, 'shop/index.html', {'brands': brands})


def products(request):
	'''Отображение всех товаров'''
	products = Product.objects.all()
	brands = Brand.objects.all()
	paginator = Paginator(products, 6, orphans=0, allow_empty_first_page=True)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {'page': page, 'products': page.object_list, 'brands': brands}
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

def product(request, product_id):
	product = Product.objects.get(pk=product_id)
	brands = Brand.objects.all()
	context = {'product': product, 'brands': brands}
	return render(request, 'shop/product.html', context)
