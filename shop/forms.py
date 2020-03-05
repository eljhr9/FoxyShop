from django import forms
from .models import Comment, Contact

class MailingForm(forms.Form):
    mailing_email = forms.EmailField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('value', 'name', 'email', 'body')

class SearchForm(forms.Form):
    query = forms.CharField()

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'body', 'image')
