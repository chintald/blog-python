# core/forms.py
from attr import fields
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)