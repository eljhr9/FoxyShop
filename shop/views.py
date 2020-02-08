from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Product, Brand, Rubric, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MailingForm, CommentForm
from django.core.mail import send_mail
from django.db.models import Avg
from cart.forms import CartAddProductForm


def mailing(request):
	if request.method == 'POST':
		form = MailingForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			subject = 'Рассылка FoxyShop'
			# message = 'Подписка на рассылку прошла успешно!'
			message = 'Приветули!'
			send_mail(subject, message, 'admin@myblog.com',[cd['email']])
			post = True
			return form, post
	else:
		form = MailingForm()
		post = False
		return form, post


def index(request):
	'''домашняя страница магазина'''
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	post = False
	form, post = mailing(request)
	context = {'brands': brands, 'rubrics': rubrics, 'form': form, 'post': post}
	return render(request, 'shop/index.html', context)


def products(request, rubric_slug=None):
	'''Отображение всех товаров'''
	products = Product.objects.all()
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	title = 'Каталог товаров'
	rubric = None

	if rubric_slug:
		rubric = get_object_or_404(Rubric, slug=rubric_slug)
		products = Product.objects.filter(rubric=rubric)
		title = rubric.name

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
	form_mailing, post = mailing(request)
	context = {'brands': brands, 'products': products, 'rubrics': rubrics,
	'title': title, 'form_mailing': form_mailing, 'post': post, 'current_rubric': rubric}
	return render(request, 'shop/products.html', context)

def brand(request):
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	form_mailing, post = mailing(request)
	context = {'brands': brands, 'rubrics': rubrics, 'form_mailing': form_mailing, 'post': post}
	return render(request, 'shop/brand.html', context)

def by_brand(request, brand_slug):
	current_brand = get_object_or_404(Brand, slug=brand_slug)
	products = Product.objects.filter(brand=current_brand)
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	title = current_brand.name
	form_mailing, post = mailing(request)
	context = {'products': products, 'brands': brands, 'rubrics': rubrics,
	'current_brand': current_brand, 'title': title, 'form_mailing': form_mailing, 'post': post}
	return render(request, 'shop/products.html', context)

def product(request, product_slug, brand_slug):
	product = get_object_or_404(Product, slug=product_slug)
	brand_slug = product.brand.slug
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	comments = product.comments.filter(is_active=True)
	review_value = Comment.objects.filter(product=product).aggregate(Avg('value'))
	sent = False
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.product = product
			new_comment.save()
			cd = comment_form.cleaned_data
			sent = True
	else:
		comment_form = CommentForm()
	form_mailing, post = mailing(request)
	similar_products = Product.objects.filter(rubric=product.rubric).exclude(id=product.id)
	cart_product_form = CartAddProductForm()
	context = {'product': product, 'brands': brands, 'rubrics': rubrics,
	'form_mailing': form_mailing, 'post': post, 'comments': comments,
	'comment_form': comment_form, 'sent': sent, 'review_value': review_value,
	'similar_products': similar_products, 'cart_product_form': cart_product_form}
	return render(request, 'shop/product.html', context)

def empty(request):
	'''Страница которая находится в разработке'''
	brands = Brand.objects.all()
	rubrics = Rubric.objects.all()
	post = False
	form, post = mailing(request)
	context = {'brands': brands, 'rubrics': rubrics, 'form': form, 'post': post}
	return render(request, 'shop/empty.html', context)
