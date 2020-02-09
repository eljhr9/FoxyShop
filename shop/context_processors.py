from .models import Brand, Rubric
from .forms import MailingForm
from django.core.mail import send_mail

def brand(request):
    brands = Brand.objects.all()
    return {'brands': brands}

def rubric(request):
    rubrics = Rubric.objects.all()
    return {'rubrics': rubrics}

def mailing(request):
	if request.method == 'POST' and 'mailing_form' in request.POST:
		mailing_form = MailingForm(request.POST)
		if mailing_form.is_valid():
			cd = mailing_form.cleaned_data
			subject = 'Рассылка FoxyShop'
			message = 'Подписка на рассылку прошла успешно!'
			send_mail(subject, message, 'FoxyShop',[cd['mailing_email']])
			post = True
			return {'mailing_form': mailing_form, 'post': post}
	else:
		mailing_form = MailingForm()
		post = False
		return {'mailing_form': mailing_form, 'post': post}
