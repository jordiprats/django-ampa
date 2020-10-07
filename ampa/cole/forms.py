from django.forms import ModelForm
from django import forms

from cole.models import *

class EditAlumneForm(ModelForm):
    class Meta:
        model = Alumne
        fields = (['nom', 'cognom1', 'cognom2', 'naixement', 'tutor1', 'telf_tutor1', 'tutor1_cessio', 'tutor2', 'telf_tutor2', 'tutor2_cessio', 'emails', 'validat' ])
        widgets = {
            'naixement': forms.DateInput(format=('%Y-%m-%d'), attrs={"type": 'date'}),
        }
        labels = {
            "nom": "Nom",
            "cognom1": "Primer cognom",
            "cognom2": "Segon cognom",
            'naixement': 'Data de naixement', 
            'tutor1': 'Primer tutor', 
            'telf_tutor1': 'Telèfon del primer tutor', 
            'tutor1_cessio': 'Cessió de dades del primer tutor', 
            'tutor2': 'Segon tutor', 
            'telf_tutor2': 'Telèfon del segon tutor', 
            'tutor2_cessio': 'Cessió de dades del segon tutor', 
            'emails': 'emails', 
            'validat': 'Firma de conformitat amb les dades'
        }