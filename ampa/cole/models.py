from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models

import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=100,
        unique=True,
    )
    email = models.EmailField(max_length=256, unique=True)
    invite = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username, allow_unicode=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nom = models.CharField(max_length=256, default='?')
    curs = models.CharField(max_length=256, default='?')

    delegat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delegatsclasses')
    subdelegat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subdelegatsclasses', blank=True, null=True)

    ultim_email = models.DateTimeField(blank=True, null=True, default=None)
    ready_to_send = models.BooleanField(default=False)

    def _get_validada(self):
        classe_validada = True
        for alumne in Alumne.objects.filter(classe=self):
            if not alumne.validat:
                classe_validada = False
        return classe_validada

    validada = property(_get_validada)

    def __str__(self):
        return self.nom+'/'+self.curs

    class Meta:
        unique_together = ('nom', 'curs', 'delegat')


class Alumne(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #id_nen         nom        cognom1     cognom2            naixement         pare      telf1       mare      telf2                                              email     cessio signatura
    num_llista = models.IntegerField()
    
    nom = models.CharField(max_length=256)
    cognom1 = models.CharField(max_length=256)
    cognom2 = models.CharField(max_length=256, default=None, blank=True, null=True)
    
    naixement = models.DateTimeField(blank=True, null=True)

    tutor1 = models.CharField(max_length=256, default='', blank=True, null=True)
    telf_tutor1 = models.CharField(max_length=256, default='', blank=True, null=True)
    tutor1_cessio = models.BooleanField(default=False, help_text="Accepto que les meves dades es facilitin al delegat i al grup classe per finalitats de comunicacions: enviament de mails, creació grup whatsapp, etc. acceptant fer un ús responsable i no facilitar a tercers les dades del grup classe que proporcionarà el delegat")

    tutor2 = models.CharField(max_length=256, default='', blank=True, null=True)
    telf_tutor2 = models.CharField(max_length=256, default='', blank=True, null=True)
    tutor2_cessio = models.BooleanField(default=False, help_text="Accepto que les meves dades es facilitin al delegat i al grup classe per finalitats de comunicacions: enviament de mails, creació grup whatsapp, etc. acceptant fer un ús responsable i no facilitar a tercers les dades del grup classe que proporcionarà el delegat")
    
    emails = models.TextField(max_length=256, default=None, blank=True, null=True)
    
    validat = models.BooleanField(default=False, help_text='He comprovat totes les dades i són correctes')

    updated_at = models.DateTimeField(auto_now=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='alumnes')

    def _get_print_name(self):
        composite_name = self.nom
        if self.cognom1:
            composite_name+=' '+self.cognom1
        if self.cognom2:
            composite_name+=' '+self.cognom2
        return composite_name

    print_name = property(_get_print_name)

    def __str__(self):
        return self._get_print_name()

    class Meta:
        unique_together = ('num_llista', 'nom', 'cognom1', 'classe')
        ordering = ['num_llista', 'classe']
        indexes = [
            models.Index(fields=['num_llista','classe']),
        ]


class FileUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    filepath = models.CharField(max_length=256)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='uploads')

    processed = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filepath

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['updated_at',]),
            models.Index(fields=['-updated_at',]),
        ]