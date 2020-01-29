from django import forms

class MailingForm(forms.Form):
    email = forms.EmailField()
