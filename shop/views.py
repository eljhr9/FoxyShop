from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Product, Brand
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
	'''домашняя страница магазина'''
	brands = Brand.objects.all()
	return render(request, 'shop/index.html', {'brands': brands})


def products(request):
	'''Отображение всех товаров'''
	products = Product.objects.all()
	brands = Brand.objects.all()
	# paginator = Paginator(products, 9)
	# if 'page' in request.GET:
	# 	page_num = request.GET['page']
	# else:
	# 	page_num = 1
	# page = paginator.get_page(page_num)
	# context = {'brands': brands, 'page': page, 'products': page.object_list}
	paginator = Paginator(products, 12)
	page = request.GET.get('page')
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		products = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		products = paginator.page(paginator.num_pages)
	# return render(request, 'shop/products.html', {"products": products, "brands": brands})
	context = {'brands': brands, 'products': products}
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
