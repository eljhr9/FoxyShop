from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Product, Brand, Rubric
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
	'''домашняя страница магазина'''
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	context = {'brands': brands, 'rubrics': rubrics}
	return render(request, 'shop/index.html', context)


def products(request):
	'''Отображение всех товаров'''
	products = Product.objects.all()
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	title = 'Каталог товаров'
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
	context = {'brands': brands, 'products': products, 'rubrics': rubrics, 'title': title}
	return render(request, 'shop/products.html', context)

def brand(request):
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	context = {'brands': brands, 'rubrics': rubrics}
	return render(request, 'shop/brand.html', context)

def by_brand(request, brand_id):
	products = Product.objects.filter(brand=brand_id)
	brands = Brand.objects.all()
	current_brand = Brand.objects.get(pk=brand_id)
	rubrics = Rubric.objects.all()
	title = current_brand.name
	context = {'products': products, 'brands': brands, 'rubrics': rubrics, 'current_brand': current_brand, 'title': title}
	return render(request, 'shop/products.html', context)

def product(request, product_id):
	product = Product.objects.get(pk=product_id)
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	context = {'product': product, 'brands': brands, 'rubrics': rubrics}
	return render(request, 'shop/product.html', context)

def by_rubric(request, rubric_id):
	products = Product.objects.filter(rubric=rubric_id)
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	current_rubric = Rubric.objects.get(pk=rubric_id)
	title = current_rubric.name
	context = {'products': products, 'rubrics': rubrics, 'brands': brands, 'current_rubric': current_rubric, 'title': title}
	return render(request, 'shop/products.html', context)
