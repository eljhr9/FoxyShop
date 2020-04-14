from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone']


class OrderDeliveryForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['city', 'address', 'postal_code']
