from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms

from cole.models import *

class InfoAlumneForm(forms.ModelForm):
    class Meta:
        model = ExtraInfoAlumne
        fields = (['descripcio', 'dades'])
        labels = {
            'descripcio': 'Descripció', 
            'dades': 'Dades (opcional)', 
        }

class ModalitatForm(forms.ModelForm):
    class Meta:
        model = Modalitat
        fields = (['name'])
        labels = {
            'name': 'Modalitat', 
        }

class EntitatForm(forms.ModelForm):
    class Meta:
        model = Entitat
        fields = (['name', 'codi_registre', 'likable_issues'])
        labels = {
            'name': 'Nom de l\'entitat',
            'codi_registre': 'Codi per registare-se',
            'likable_issues': 'Votació de peticions'
        }

class CursForm(forms.ModelForm):
    class Meta:
        model = Curs
        fields = (['curs', 'modalitat'])
        labels = {
            'curs': 'Anys del curs', 
            'modalitat': 'Modalitat'
        }

class EtapaForm(forms.ModelForm):
    class Meta:
        model = Etapa
        fields = (['nom', 'ordre'])
        labels = {
            'nom': 'Nom de la etapa',
            'ordre': 'Ordre de la etapa'
        }

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
        fields = (['nom', 'alias', 'curs', 'etapa', 'tutor', 'nom_delegat', 'telefon_delegat', 'email_delegat', 'nom_subdelegat', 'telefon_subdelegat', 'email_subdelegat'])
        labels = {
            'nom': 'Classe', 
            'alias': 'Nom de la classe', 
            'curs': 'Curs escolar',
            'etapa': 'Etapa',
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

class StaffClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = (['nom', 'alias', 'curs', 'etapa', 'delegat', 'subdelegat', 'tutor', 'nom_delegat', 'telefon_delegat', 'email_delegat', 'nom_subdelegat', 'telefon_subdelegat', 'email_subdelegat'])
        labels = {
            'nom': 'Classe', 
            'alias': 'Nom de la classe', 
            'curs': 'Curs escolar',
            'etapa': 'Etapa',
            'delegat': 'Delegat',
            'subdelegat': 'Subdelegat',
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
    def __init__(self, *args, **kwargs):
        staff_view = kwargs.pop('staff_view',None)
        super(EditAlumneForm, self).__init__(*args, **kwargs)
        if not staff_view:
            self.fields['alta'].disabled = True
            self.fields['baixa'].disabled = True

    class Meta:
        model = Alumne
        fields = ([ 'num_llista', 'nom', 'cognom1', 'cognom2', 'naixement', 'alta', 'baixa', 'tutor1', 'telf_tutor1', 'email_tutor1', 'tutor2', 'telf_tutor2', 'email_tutor2' ])
        widgets = {
            'naixement': forms.DateInput(format=('%Y-%m-%d'), attrs={"type": 'date'}),
            'alta': forms.DateInput(format=('%Y-%m-%d'), attrs={"type": 'date'}),
            'baixa': forms.DateInput(format=('%Y-%m-%d'), attrs={"type": 'date'}),
        }
        labels = {
            'num_llista': 'Numero de la llista',
            "nom": "Nom",
            "cognom1": "Primer cognom",
            "cognom2": "Segon cognom",
            'naixement': 'Data de naixement',
            'alta': 'Data d\'alta',
            'baixa': 'Data de baixa',
            'tutor1': 'Primer tutor', 
            'telf_tutor1': 'Telèfon del primer tutor', 
            'email_tutor1': 'eMail tutor 1',
            'tutor2': 'Segon tutor', 
            'telf_tutor2': 'Telèfon del segon tutor', 
            'email_tutor2': 'eMail tutor 2',
        }

class EditAlumneParesForm(ModelForm):
    class Meta:
        model = Alumne
        fields = (['nom', 'cognom1', 'cognom2', 'naixement', 'tutor1', 'telf_tutor1', 'email_tutor1', 'tutor1_cessio', 'tutor2', 'telf_tutor2', 'email_tutor2', 'tutor2_cessio', 'validat' ])
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
            'email_tutor1': 'eMail tutor 1',
            'tutor1_cessio': 'Cessió de dades del primer tutor', 
            'tutor2': 'Segon tutor', 
            'telf_tutor2': 'Telèfon del segon tutor', 
            'email_tutor2': 'eMail tutor 2',
            'tutor2_cessio': 'Cessió de dades del segon tutor', 
            'emails': 'emails', 
            'validat': 'Firma de conformitat amb les dades'
        }

def validate_user_email_doesnt_exists(value):
    user = User.objects.filter(email=value.lower())
    if user:
        raise ValidationError('email already registered') 

class WIUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_user_email_doesnt_exists])

    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2", "invite")
        labels = {
            "email": "email",
            "invite": "codi d'activació",
        }
    def save(self, commit=True):
        config = Entitat.objects.first()
        if self.cleaned_data["invite"] == config.codi_registre:
            user = super(WIUserCreationForm, self).save(commit=False)
            user.username = user.email = self.cleaned_data["email"].lower()
            if commit:
                user.save()
            return user
        else:
            return None

class AdminEditUser(ModelForm):
    class Meta:
        model = User
        fields = (['name', 'representant', 'is_staff'])
        labels = {
            'name': 'Nom',
            'is_staff': 'Administrador',
            'representant': 'Funció principal'
        }



class AMPAUserName(forms.Form):
    name = forms.CharField(label='Nom d\'usuari')

    def __init__(self, data, **kwargs):
        initial = kwargs.get('initial', {})
        data = {**initial, **data}
        super().__init__(data, **kwargs)

    def clean(self):
        try:
            name = self.data['name'][0]
        except:
            return
    class Meta:
        fields = (['name'])

class PasswordChangeForm(forms.Form):
    password_actual = forms.CharField(label='Contrasenya actual', required=False, widget=forms.PasswordInput)
    password1 = forms.CharField(label='Contrasenya', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeteix contrasenya', required=False, widget=forms.PasswordInput)

    def __init__(self, data, **kwargs):
        initial = kwargs.get('initial', {})
        data = {**initial, **data}
        super().__init__(data, **kwargs)

    def clean(self):
        try:
            actual = self.data['password_actual'][0]
            password1 = self.data['password1'][0]
            password2 = self.data['password2'][0]
        except:
            return

        if not password1:
            raise forms.ValidationError(
                'Si us plau, defineix una contrasenya',
                code='change_password_password_not_set'
            )            

        if password1 != password2:
            raise forms.ValidationError(
                'Les contrasenyes no coincideixen',
                code='change_password_password_does_not_match'
            )

        if len(password1) < 5:
            raise forms.ValidationError(
                'La contrasenya ha de ser de 5 caracters mínim',
                code='change_password_password_too_short'
            )
        
    class Meta:
        fields = (['password1', 'password2'])

class AreYouSureForm(forms.Form):
    pass