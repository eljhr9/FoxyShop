from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(template_name='shop/index.html'), name='logout'), #  template_name='users/logout.html'
    path('logout/', views.logout_view, name='logout'),
]
