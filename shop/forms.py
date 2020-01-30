from django import forms
from .models import Comment

class MailingForm(forms.Form):
    email = forms.EmailField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('value', 'name', 'email', 'body')
