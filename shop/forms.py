from django import forms
from .models import Comment

class MailingForm(forms.Form):
    mailing_email = forms.EmailField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('value', 'name', 'email', 'body')

class SearchForm(forms.Form):
    query = forms.CharField()
