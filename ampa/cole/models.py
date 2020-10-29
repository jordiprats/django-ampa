from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
from django.db import models

import uuid
import re

MAILING_STATUS_DRAFT = '0'
MAILING_STATUS_PROGRAMAT = '1'
MAILING_STATUS_ENVIANT = '2'
MAILING_STATUS_ENVIAT = '3'
MAILING_STATUS = [
    (MAILING_STATUS_DRAFT, 'borrador'),
    (MAILING_STATUS_PROGRAMAT, 'enviament programat'),
    (MAILING_STATUS_ENVIANT, 'enviant...'),
    (MAILING_STATUS_ENVIAT, 'enviament completat')
]


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

    nom = models.CharField(max_length=256, default='')
    curs = models.CharField(max_length=256, default='')

    delegat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delegatsclasses')
    subdelegat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subdelegatsclasses', blank=True, null=True)

    ultim_email = models.DateTimeField(blank=True, null=True, default=None)
    ready_to_send = models.BooleanField(default=False)

    latest_export = models.CharField(max_length=256, blank=True, null=True, default=None)
    waiting_export = models.BooleanField(default=False)

    tutor = models.CharField(max_length=256, blank=True, null=True, default='')
    
    nom_delegat = models.CharField(max_length=256, blank=True, null=True, default='')
    telefon_delegat = models.CharField(max_length=256, blank=True, null=True, default='')
    email_delegat = models.CharField(max_length=256, blank=True, null=True, default='')

    nom_subdelegat = models.CharField(max_length=256, blank=True, null=True, default='')
    telefon_subdelegat = models.CharField(max_length=256, blank=True, null=True, default='')
    email_subdelegat = models.CharField(max_length=256, blank=True, null=True, default='')

    def _get_validada(self):
        classe_validada = True
        for alumne in Alumne.objects.filter(classe=self):
            if not alumne.validat:
                classe_validada = False
        return classe_validada

    validada = property(_get_validada)

    def _is_procesant(self):
        return self.alumnes.count() == 0 and self.uploads.count() != 0

    is_procesant = property(_is_procesant)

    def _is_upload_error(self):
        return self.uploads.filter(error=True).count() > 0 and self.uploads.filter(error=False, processed=True).count() == 0

    is_upload_error = property(_is_upload_error)

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

    def _get_mailing_emails(self):
        if self.tutor1_cessio and self.tutor2_cessio and self.validat:
            return re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.emails.lower())
        else:
            return []
    
    mailing_emails = property(_get_mailing_emails)

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

class FileAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    filename = models.CharField(max_length=256)
    upload_path = models.CharField(max_length=256)
    filepath = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _is_image(self):
        return re.match('.jpg$', filename) or re.match('.jpeg$', filename) or re.match('.png$', filename)

    is_image = property(_is_image)

    def _get_url(self):
        return 'uploads/'+self.upload_path+'/'+self.filename

    url = property(_get_url)

    def __str__(self):
        return self.filename
    
    def delete(self, *args, **kwargs):
        try:
            os.remove(self.filepath)
        except:
            pass
        super(FileAttachment, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at',]),
        ]

class Mailing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    #subject, html_message, email_from, email_reply_to, recipient_list
    subject = models.CharField(max_length=256)
    html_message = models.TextField(max_length=10000, default=None, blank=True, null=True)
    email_from = models.CharField(max_length=256, default='')
    email_reply_to = models.CharField(max_length=256, default=None)

    classes = models.ManyToManyField(Classe, related_name='mailings')
    attachments = models.ManyToManyField(FileAttachment, related_name='mailings')
    nomes_delegats = models.BooleanField(default=False)

    status = models.CharField(
        max_length=1,
        choices=MAILING_STATUS,
        default=MAILING_STATUS_DRAFT,
    )
    progress = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _get_recipient_emails(self):
        mailing_emails = set()
        for classe in self.classes.all():
            for alumne in classe.alumnes.all():
                for email in alumne.mailing_emails:
                    mailing_emails.add(email)
        return mailing_emails
    
    recipient_list = property(_get_recipient_emails)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-updated_at', 'status']
        indexes = [
            models.Index(fields=['-updated_at', 'status']),
            models.Index(fields=['status']),
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
