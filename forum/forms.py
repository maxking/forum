from django import forms
from wiki.forum.models import post
from django.forms.util import ErrorList


class PostForm(forms.Form):
    title = forms.CharField(max_length = 150, label ='Title-')
    message = forms.CharField(label = 'Message-', widget=forms.Textarea)

class CommentForm(forms.Form):
    message = forms.CharField(label = 'Comment', widget = forms.Textarea)
