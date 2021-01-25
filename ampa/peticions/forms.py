from django.forms import ModelForm
from django import forms

from peticions.models import *

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (['titol', 'categories', 'html_message'])
        labels = {
            'titol': 'Titol petició',
            'categories': 'Categories',
            'html_message': 'Descripció',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (['html_message'])
        labels = {
            'html_message': 'Comentari',
        }

class CategoryForm(forms.ModelForm):
    name = forms.TextInput(attrs={'size': '40'})
    
    class Meta:
        model = Category
        fields = (['name'])
        labels = {
            'name': 'Nom de la categoria', 
        }