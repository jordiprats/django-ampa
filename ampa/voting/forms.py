from django.forms import ModelForm
from django import forms

from voting.models import *

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = (['titol', 'html_message'])
        labels = {
            'titol': 'Titol', 
            'html_message': 'Missatge', 
        }

class OptionForm(forms.ModelForm):
    text = forms.TextInput(attrs={'size': '40'})
    
    class Meta:
        model = Option
        fields = (['text', 'order'])
        labels = {
            'text': 'Text de l\'opció', 
            'order': 'Ordre', 
        }