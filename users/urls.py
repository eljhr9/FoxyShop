from django.urls import path
from django.urls import reverse_lazy
import django.contrib.auth.views as user
from . import views

# app_name = 'account'

urlpatterns = [
    path('login/', user.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', user.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password-change/done/', user.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('password-reset/', user.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name="password_reset"),
	path('password-reset/done/', user.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
	path('reset/<uidb64>/<token>/', user.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name="password_reset_confirm"),
	path('reset/done/', user.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path('register/', views.register, name="register"),
    path('edit/', views.edit, name="edit_profile"),
    path('history/', views.purchase_history, name="purchase_history"),
]
