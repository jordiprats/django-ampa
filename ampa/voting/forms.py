from django.forms import ModelForm
from django import forms

from voting.models import *

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = (['titol', 'html_message', 'multianswer', 'anonymous'])
        labels = {
            'titol': 'Titol', 
            'html_message': 'Missatge', 
            'multianswer': 'Multiresposta',
            'anonymous': 'Enquesta anònima'
        }

class OptionForm(forms.ModelForm):
    text = forms.TextInput(attrs={'size': '40'})
    
    class Meta:
        model = Option
        fields = (['text', 'order'])
        labels = {
            'text': 'Text de l\'opció', 
            'order': 'Ordre en la llista de opcions', 
        }