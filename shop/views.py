from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Product, Brand, Rubric, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, SearchForm, ContactForm
from django.db.models import Avg
from cart.forms import CartAddProductForm
from haystack.query import SearchQuerySet
from django.core.mail import send_mail
from django.contrib import messages
from .recommender import Recommender


def index(request):
	'''домашняя страница магазина'''
	products = Product.objects.all()[:8]
	discount_products = Product.objects.all().exclude(discount=0)[:8]
	context = {'title': 'Главная', 'products': products, 'discount_products': discount_products}
	return render(request, 'shop/index.html', context)


def products(request, rubric_slug=None, brand_slug=None):
	'''Отображение всех товаров'''
	products = Product.objects.all()
	title = 'Каталог товаров'
	rubric = None
	brand = None
	brand_page = False
	language = request.LANGUAGE_CODE
	if request.method == 'POST' and 'price-' in request.POST:
		products.order_by('-price')

	if rubric_slug:
		rubric = get_object_or_404(Rubric, translations__language_code=language, translations__slug=rubric_slug)
		products = Product.objects.filter(rubric=rubric)
		title = rubric.name

	if brand_slug:
		brand_page = True
		brand = get_object_or_404(Brand, slug=brand_slug)
		products = Product.objects.filter(brand=brand)
		title = brand.name

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
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	cart_product_form = CartAddProductForm()
	context = {'products': products, 'title': title, 'current_rubric': rubric,
	'cart_product_form': cart_product_form, 'page': page, 'brand_page': brand_page}
	return render(request, 'shop/products.html', context)

def brand(request):
	context = {'brand_page': True}
	return render(request, 'shop/brand.html', context)


def product(request, product_slug, brand_slug):
	product = get_object_or_404(Product, slug=product_slug)
	brand_slug = product.brand.slug
	comments = product.comments.filter(is_active=True)
	review_value = Comment.objects.filter(product=product).aggregate(Avg('value'))
	sent = False
	is_favourite = False
	title = product.rubric.name
	if product.favourite.filter(id=request.user.id).exists():
		is_favourite = True

	if request.method == 'POST' and 'comment' in request.POST:
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.product = product
			new_comment.save()
			cd = comment_form.cleaned_data
			sent = True
	else:
		comment_form = CommentForm()
	r = Recommender()
	similar_products = r.suggest_products_for([product], 4)
	if not similar_products:
		similar_products = Product.objects.filter(rubric=product.rubric).exclude(id=product.id)[:4]
	cart_product_form = CartAddProductForm()
	context = {'product': product, 'comments': comments, 'comment_form': comment_form,
	'sent': sent, 'review_value': review_value, 'similar_products': similar_products,
	'cart_product_form': cart_product_form, 'is_favourite': is_favourite, 'title': title}
	return render(request, 'shop/product.html', context)

def empty(request):
	'''Страница которая находится в разработке'''
	context = {}
	return render(request, 'shop/empty.html', context)

def product_search(request):
	search_form = SearchForm()
	cd = None
	results = None
	total_results = None
	if 'query' in request.GET:
		search_form = SearchForm(request.GET)
		if search_form.is_valid():
			cd = search_form.cleaned_data
			results = SearchQuerySet().models(Product).filter(content=cd['query']).load_all()
			total_results = results.count()
	context = {'search_form': search_form, 'cd': cd, 'results': results, 'total_results': total_results}
	return render(request, 'shop/search.html', context)

def discount(request):
	products = Product.objects.all().exclude(discount=0)
	title = 'Акционные товары'
	context = {'products': products, 'title': title}
	return render(request, 'shop/products.html', context)

def new(request):
	# products = Product.objects.all().exclude(discount=0)
	title = 'Новинки'
	context = {'title': title}
	return render(request, 'shop/new_products.html', context)

@login_required
def favourite_add(request, id):
	product = get_object_or_404(Product, id=id)
	if product.favourite.filter(id=request.user.id).exists():
		product.favourite.remove(request.user)
	else:
		product.favourite.add(request.user)
	return HttpResponseRedirect(product.get_absolute_url())

@login_required
def favourite_list(request):
	user = request.user
	favourite = user.favourite.all()
	context = {'favourite': favourite}
	return render(request, 'shop/favourite.html', context)

def contacts(request):
	if request.method == 'POST' and 'contact_form' in request.POST:
		contact_form = ContactForm(request.POST, request.FILES)
		if contact_form.is_valid():
			new_contact = contact_form.save()
			subject = 'Обратная связь FoxyShop'
			if new_contact.image:
				message = f'Сообщение от пользователя \"{new_contact.name}\".\n\n\t{new_contact.body}. \
				\nСсылка на скриншот - {new_contact.image.url} \nEmail пользователя - {new_contact.email}.'
			else:
				message = f'Сообщение от пользователя \"{new_contact.name}\".\n\n\t{new_contact.body}. \
				\nСсылка на скриншот отсутсвует! \nEmail пользователя - {new_contact.email}.'
			send_mail(subject, message, 'FoxyShop', ['foxymailing@gmail.com'])
			message_send = True
			messages.success(request, 'Ваше сообщение было отправлено!')
			contact_form = ContactForm()
		else:
			messages.error(request, 'Произойшла ошибка, попробуйте снова.')
	else:
		contact_form = ContactForm()
		message_send = False
	context = {'title': 'Контакты', 'contact_form': contact_form, 'message_send': message_send}
	return render(request, 'shop/contacts.html', context)

def delivery(request):
	context = {'title': 'Доставка'}
	return render(request, 'shop/delivery.html', context)
