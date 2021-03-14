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
            'html_message': 'Descripció',
        }

class IssueAdminForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (['titol', 'owner', 'representant', 'categories', 'public', 'status', 'html_message'])
        labels = {
            'titol': 'Titol petició',
            'owner': 'Autor',
            'representant': 'Mostra la petició feta com a representant de:',
            'categories': 'Categories',
            'public': 'publicat',
            'destacada': 'Destacar petició',
            'status': 'Estat',
            'html_message': 'Descripció',
        }
        widgets = {
            'owner': forms.Select(attrs={'disabled':'disabled'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (['internal', 'html_message'])
        labels = {
            'internal': 'restringir',
            'html_message': 'Comentari',
        }

class AdminCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (['user', 'representant', 'internal', 'html_message'])
        labels = {
            'representant': 'Mostra el comentari fet en nom de:',
            'internal': 'restringir',
            'user': 'Autor',
            'html_message': 'Comentari',
        }
        widgets = {
            'user': forms.Select(attrs={'disabled':'disabled'})
        }

class JuntaPeuForm(forms.ModelForm):
    class Meta:
        model = Junta
        fields = (['peu_message'])
        labels = {
            'peu_message': 'Text',
        }

class JuntaForm(forms.ModelForm):
    class Meta:
        model = Junta
        fields = (['name', 'celebracio', 'public', 'html_message'])
        widgets = {
            'celebracio': forms.DateInput(format=('%Y-%m-%d'), attrs={"type": 'date'}),
        }
        labels = {
            'name': 'Junta',
            'celebracio': 'Data de celebració',
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

class RepresentantForm(forms.ModelForm):
    name = forms.TextInput(attrs={'size': '40'})
    
    class Meta:
        model = Representant
        fields = (['name'])
        labels = {
            'name': 'Representant',
        }