from django import forms
from django.contrib.auth.models import User
from .models import Profile, Delivery

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        unique_together = [['email']]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не сходятся!')
        return cd['password2']

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('phone_number', 'avatar')

class DeliveryEditForm(forms.ModelForm):
	class Meta:
		model = Delivery
		fields = ('city', 'address', 'postal_code')
