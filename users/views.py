from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))

    else:
         user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'users/login.html', {'form': form})
