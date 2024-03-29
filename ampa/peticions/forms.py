from django.forms import ModelForm
from django import forms

from peticions.models import *

class IssueFilterForm(forms.Form):
    status_filter = forms.ChoiceField(choices=ISSUE_STATUS, required = False)

    def __init__(self, data, **kwargs):
        initial = kwargs.get('initial', {})
        data = {**initial, **data}
        super().__init__(data, **kwargs)

    def clean(self):
        try:
            status_filter = self.data['status_filter'][0]
        except:
            return
    class Meta:
        fields = (['status_filter'])
        labels = {
            'status_filter': 'Estat de la petició',
        }

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (['titol', 'categories', 'html_message'])
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
        fields = (['name', 'celebracio', 'public', 'html_message', 'wordtemplate'])
        widgets = {
            'celebracio': forms.DateInput(format=('%Y-%m-%d'), attrs={"type": 'date'}),
        }
        labels = {
            'name': 'Junta',
            'celebracio': 'Data de celebració',
            'public': 'Publicar',
            'html_message': 'Text',
            'wordtemplate': 'Plantilla',
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