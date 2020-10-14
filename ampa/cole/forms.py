from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
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

class WIUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2", "invite")
        labels = {
            "email": "email",
            "invite": "codi d'activació",
        }
    def save(self, commit=True):
        if self.cleaned_data["invite"] == 'lestodelegats':
            user = super(WIUserCreationForm, self).save(commit=False)
            user.username = user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            return user
        else:
            return None

class AreYouSureForm(forms.Form):
    pass