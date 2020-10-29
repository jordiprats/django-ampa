from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms

from cole.models import *

class ClasseMailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = (['subject', 'html_message'])
        labels = {
            'subject': 'Asumpte', 
            'html_message': 'Missatge', 
        }

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = (['nom', 'curs', 'tutor', 'nom_delegat', 'telefon_delegat', 'email_delegat', 'nom_subdelegat', 'telefon_subdelegat', 'email_subdelegat'])
        labels = {
            'nom': 'Nom de la classe', 
            'curs': 'Curs escolar', 
            'tutor:': 'Nom tutor de la classe', 
            'nom_delegat': 'Nom del delegat', 
            'telefon_delegat': 'Telèfon del delegat', 
            'email_delegat': 'e-Mail del delegat', 
            'nom_subdelegat': 'Nom del subdelegat', 
            'telefon_subdelegat': 'Telèfon del subdelegat', 
            'email_subdelegat': 'e-Mail del subdelegat',
            'subject': 'Asumpte', 
            'html_message': 'Missatge', 
        }

class EditAlumneForm(ModelForm):
    class Meta:
        model = Alumne
        fields = ([ 'num_llista', 'nom', 'cognom1', 'cognom2', 'naixement', 'tutor1', 'telf_tutor1', 'tutor2', 'telf_tutor2', 'emails' ])
        widgets = {
            'naixement': forms.DateInput(format=('%Y-%m-%d'), attrs={"type": 'date'}),
        }
        labels = {
            'num_llista': 'Numero de la llista',
            "nom": "Nom",
            "cognom1": "Primer cognom",
            "cognom2": "Segon cognom",
            'naixement': 'Data de naixement', 
            'tutor1': 'Primer tutor', 
            'telf_tutor1': 'Telèfon del primer tutor', 
            'tutor2': 'Segon tutor', 
            'telf_tutor2': 'Telèfon del segon tutor', 
            'emails': 'emails', 
        }

class EditAlumneParesForm(ModelForm):
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