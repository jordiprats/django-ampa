from django.forms import ModelForm
from django import forms

from peticions.models import *

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (['titol', 'categories', 'public', 'html_message'])
        labels = {
            'titol': 'Titol petició',
            'categories': 'Categories',
            'public': 'publicat',
            'html_message': 'Descripció',
        }

class IssueAdminForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (['titol', 'categories', 'public', 'status', 'html_message'])
        labels = {
            'titol': 'Titol petició',
            'categories': 'Categories',
            'public': 'publicat',
            'status': 'Estat',
            'html_message': 'Descripció',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (['internal', 'html_message'])
        labels = {
            'internal': 'restringir',
            'html_message': 'Comentari',
        }

class JuntaForm(forms.ModelForm):
    class Meta:
        model = Junta
        fields = (['name', 'public', 'html_message'])
        labels = {
            'name': 'Junta',
            'public': 'Publicar',
            'html_message': 'Text',
        }

class CategoryForm(forms.ModelForm):
    name = forms.TextInput(attrs={'size': '40'})
    
    class Meta:
        model = Category
        fields = (['name', 'ordre'])
        labels = {
            'name': 'Nom de la categoria', 
            'ordre': 'Ordre'
        }