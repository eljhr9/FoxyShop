from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from orders.models import Order
from django.contrib import messages


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли с аккаунта')
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))

    else:
         user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})


@login_required
def edit(request):
    profile = Profile.objects.filter(user=request.user)
    if not profile:
        person = Profile.objects.create(user=request.user)
    if request.method == 'POST' and 'edit_form' in request.POST:
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Изменения сохранены')
        else:
            messages.error(request, 'Произойшла ошибка, попробуйте снова')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    title = 'edit'
    context = {'user_form': user_form, 'profile_form': profile_form, 'title': title}
    return render(request, 'users/edit.html', context)

@login_required
def purchase_history(request):
    orders = Order.objects.filter(user=request.user)
    title = 'history'
    context = {'title': title, 'orders': orders}
    return render(request, 'users/history.html', context)
