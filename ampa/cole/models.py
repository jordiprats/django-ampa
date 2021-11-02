from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse
from django.db import models

import unidecode
import uuid
import re

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

    name = models.CharField(max_length=256, blank=True, null=True, default='')
    representant = models.ForeignKey('peticions.Representant', on_delete=models.SET_NULL, related_name='users', default=None, blank=True, null=True)

    last_login = models.DateTimeField(auto_now=True)

    is_default_password = models.BooleanField(default=False)
    last_password_change = models.DateTimeField(default=None, blank=True, null=True)

    is_locked = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()     
        self.slug = slugify(self.username, allow_unicode=False)
        super().save(*args, **kwargs)
        try:
            classes_delegat = Classe.objects.filter(email_delegat__iexact=self.email)
            for classe in classes_delegat:
                classe.save()

            classes_subdelegat = Classe.objects.filter(email_subdelegat__iexact=self.email)
            for classe in classes_subdelegat:
                classe.save()
        except:
            pass

    class Meta:
        ordering = ['email']
        indexes = [
            models.Index(fields=['email']),
        ]

class Modalitat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    ordre = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordre']
        indexes = [
            models.Index(fields=['ordre']),
        ]

class Curs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curs = models.CharField(max_length=256, default='')

    modalitat = models.ForeignKey(Modalitat, on_delete=models.CASCADE, related_name='cursos', blank=True, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.modalitat:
            return self.curs+'/'+str(self.modalitat)
        else:
            return self.curs

    class Meta:
        unique_together = ('curs', 'modalitat')
        ordering = ['-curs']
        indexes = [
            models.Index(fields=['curs']),
        ]

class Etapa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=256, default='')
    ordre = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['ordre', 'nom']
        indexes = [
            models.Index(fields=['nom']),
        ]

class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nom = models.CharField(max_length=256, default='')
    alias = models.CharField(max_length=256, default='', blank=True, null=True,)

    curs = models.ForeignKey(Curs, on_delete=models.CASCADE, related_name='classes', blank=True, null=True, default=None)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, related_name='classes', blank=True, null=True, default=None)

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

    def _get_full_nom(self):
        try:
            if self.alias:
                str_nom = self.nom+' ('+self.alias+')'
            else:
                str_nom =  self.nom
            return str_nom
        except:
            return str(self.id)

    full_nom = property(_get_full_nom)

    def __str__(self):
        return self._get_full_nom()

    def save(self, *args, **kwargs):
        if self.email_delegat:
            self.email_delegat = self.email_delegat.lower().strip()

            delegat = User.objects.filter(email__iexact=self.email_delegat).first()
            if delegat:
                self.delegat = delegat

        if self.email_subdelegat:
            self.email_subdelegat = self.email_subdelegat.lower().strip()
        
            subdelegat = User.objects.filter(email__iexact=self.email_subdelegat).first()
            if subdelegat:
                self.subdelegat = subdelegat
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-curs', 'etapa','nom']
        unique_together = ('nom', 'curs', 'etapa', 'delegat')

class Alumne(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #id_nen         nom        cognom1     cognom2            naixement         pare      telf1       mare      telf2                                              email     cessio signatura
    # TODO: petar num_llista
    num_llista = models.IntegerField(default=0)
    
    nom = models.CharField(max_length=256)
    cognom1 = models.CharField(max_length=256)
    cognom2 = models.CharField(max_length=256, default=None, blank=True, null=True)

    nom_unaccented = models.CharField(max_length=256, default="", blank=True, null=True)
    cognom1_unaccented = models.CharField(max_length=256, default="", blank=True, null=True)
    cognom2_unaccented = models.CharField(max_length=256, default="", blank=True, null=True)
    
    naixement = models.DateTimeField(default=None, blank=True, null=True)

    tutor1 = models.CharField(max_length=256, default='', blank=True, null=True)
    telf_tutor1 = models.CharField(max_length=256, default='', blank=True, null=True)
    email_tutor1 = models.TextField(max_length=600, default=None, blank=True, null=True)
    tutor1_cessio = models.BooleanField(default=False, help_text="Accepto que les meves dades es facilitin al delegat i al grup classe per finalitats de comunicacions: enviament de mails, creació grup whatsapp, etc. acceptant fer un ús responsable i no facilitar a tercers les dades del grup classe que proporcionarà el delegat")

    tutor2 = models.CharField(max_length=256, default='', blank=True, null=True)
    telf_tutor2 = models.CharField(max_length=256, default='', blank=True, null=True)
    email_tutor2 = models.TextField(max_length=600, default=None, blank=True, null=True)
    tutor2_cessio = models.BooleanField(default=False, help_text="Accepto que les meves dades es facilitin al delegat i al grup classe per finalitats de comunicacions: enviament de mails, creació grup whatsapp, etc. acceptant fer un ús responsable i no facilitar a tercers les dades del grup classe que proporcionarà el delegat")
    
    alta = models.DateTimeField(blank=True, null=True)
    baixa = models.DateTimeField(blank=True, null=True)

    validat = models.BooleanField(default=False, help_text='He comprovat totes les dades i són correctes')

    updated_at = models.DateTimeField(auto_now=True)
    classes = models.ManyToManyField(Classe, related_name='alumnes')

    def _get_cessio_emails(self):
        emails = []
        if self.email_tutor1:
            emails += re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.email_tutor1.lower().strip())
        if self.email_tutor2:
            emails += re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.email_tutor2.lower().strip())

        return emails

    cessio_emails = property(_get_cessio_emails)

    def _get_mailing_emails(self):
        emails = []
        if self.tutor1_cessio:
            emails += re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.email_tutor1.lower().strip())
        
        if self.tutor2_cessio:
            emails += re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.email_tutor2.lower().strip())

        return emails

    mailing_emails = property(_get_mailing_emails)

    def _get_print_name(self):
        composite_name = self.nom
        if self.cognom1:
            composite_name+=' '+self.cognom1
        if self.cognom2:
            composite_name+=' '+self.cognom2
        return composite_name

    print_name = property(_get_print_name)

    def _get_classe_actual(self):
        try:
            return self.classes.order_by('curs').first()
        except:
            return None

    classe = property(_get_classe_actual)

    def _get_extrainfo_hash(self):
        attachments_dict = {}
        if self.extrainfo:
            for extrainfo in self.extrainfo.all():
                if extrainfo.attachment:
                    if extrainfo.descripcio:
                        attachments_dict[extrainfo.descripcio] = extrainfo.id
                    else:
                        attachments_dict[extrainfo.attachment.filename] = extrainfo.id
                else:
                    if extrainfo.descripcio:
                        attachments_dict[extrainfo.descripcio] = extrainfo.id
                    else:
                        attachments_dict[str(extrainfo.id)] = extrainfo.id        
        return attachments_dict

    extrainfo_hash = property(_get_extrainfo_hash)

    def save(self, *args, **kwargs):
        if self.nom:
            self.nom_unaccented = unidecode.unidecode(self.nom.replace('·', '.')).lower()
        if self.cognom1:
            self.cognom1_unaccented = unidecode.unidecode(self.cognom1.replace('·', '.')).lower()
        if self.cognom2:
            self.cognom2_unaccented = unidecode.unidecode(self.cognom2.replace('·', '.')).lower()
        if self.telf_tutor1:
            self.telf_tutor1 = self.telf_tutor1.replace(" ", "")
        if self.telf_tutor2:
            self.telf_tutor2 = self.telf_tutor2.replace(" ", "")
        super().save(*args, **kwargs)

    def __str__(self):
        return self._get_print_name()

    class Meta:
        ordering = ['num_llista', 'cognom1', 'cognom2' ]

class FileAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    filename = models.CharField(max_length=256)
    upload_path = models.CharField(max_length=256)
    filepath = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _is_image(self):
        return re.search('\.jpg$', self.filename) or re.search('\.jpeg$', self.filename) or re.search('\.png$', self.filename)

    is_image = property(_is_image)

    def _get_static_url(self):
        return settings.STATIC_DOMAIN+'uploads/'+self.upload_path+'/'+self.filename

    static_url = property(_get_static_url)

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

class ExtraInfoAlumne(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    alumne = models.ForeignKey(Alumne, on_delete=models.CASCADE, related_name='extrainfo')

    descripcio = models.CharField(max_length=256, default='', blank=True, null=True)

    dades = models.TextField(max_length=600, default='', blank=True, null=True)
    attachment = models.ForeignKey(FileAttachment, on_delete=models.CASCADE, related_name='files', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['updated_at',]),
            models.Index(fields=['-updated_at',]),
        ]

MAILING_STATUS_DRAFT = '0'
MAILING_STATUS_PROGRAMAT = '1'
MAILING_STATUS_ENVIANT = '2'
MAILING_STATUS_ENVIAT = '3'
MAILING_STATUS_ERROR_GENERAL = 'E'
MAILING_STATUS = [
    (MAILING_STATUS_DRAFT, 'borrador'),
    (MAILING_STATUS_PROGRAMAT, 'enviament programat'),
    (MAILING_STATUS_ENVIANT, 'enviant...'),
    (MAILING_STATUS_ENVIAT, 'completat'),
    (MAILING_STATUS_ERROR_GENERAL, 'error general d\'enviament')
]

class Mailing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    #subject, html_message, email_from, email_reply_to, recipient_list
    subject = models.CharField(max_length=256)
    html_message = models.TextField(max_length=10000, default=None, blank=True, null=True)
    email_from = models.CharField(max_length=256, default=None, blank=True, null=True)
    email_reply_to = models.CharField(max_length=256, default=None, blank=True, null=True)

    classes = models.ManyToManyField(Classe, related_name='mailings')
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, related_name='mailings', blank=True, null=True, default=None)
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE, related_name='mailings', blank=True, null=True, default=None)

    attachments = models.ManyToManyField(FileAttachment, related_name='mailings')
    nomes_delegats = models.BooleanField(default=False)

    status = models.CharField(
        max_length=1,
        choices=MAILING_STATUS,
        default=MAILING_STATUS_DRAFT,
    )
    progress = models.IntegerField(default=0)

    #emails_sent = ArrayField(models.CharField(max_length=200))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _get_recipient_emails(self):
        mailing_emails = set()
        classes = self.classes.all()
        for classe in classes:
            for alumne in classe.alumnes.all():
                for email in alumne.mailing_emails:
                    mailing_emails.add(email)
        return mailing_emails
    
    recipient_list = property(_get_recipient_emails)

    def _get_local_attachment_hash(self):
        attachments_dict = {}
        for attachment in self.attachments.all():
            attachments_dict[attachment.filename] = attachment.filepath
        return attachments_dict

    localfile_attachment_hash = property(_get_local_attachment_hash)

    def _get_attachment_hash(self):
        attachments_dict = {}
        for attachment in self.attachments.all():
            attachments_dict[attachment.filename] = attachment.static_url
        return attachments_dict

    attachment_hash = property(_get_attachment_hash)

    def _get_images_hash(self):
        attachments_dict = {}
        for attachment in self.attachments.all():
            if attachment.is_image:
                attachments_dict[attachment.filename] = attachment.static_url
        return attachments_dict

    images_hash = property(_get_images_hash)

    def get_manual_unsubscribe_links(self, email):
        links = set()
        for classe in self.classes.all():
            for alumne in classe.alumnes.all():
                if email in alumne.mailing_emails:
                    url = reverse('form.pares.edit.alumne', kwargs={ 'alumne_id': alumne.id })
                    links.add(url)
        return links

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

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads', blank=True, null=True, default=None)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='uploads', blank=True, null=True, default=None)

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

class EmailSent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='sent', blank=True, null=True, default=None)
    email = models.EmailField(max_length=256)

    sent = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    where = models.TextField(max_length=10000, default='', blank=True, null=True)
    what = models.TextField(max_length=10000, default='', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ???
class DocumentTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    html_message = models.TextField(max_length=50000, default='', blank=True, null=True)

class WordTemplate(FileAttachment):
    pass

class Entitat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, blank=True, null=True, default='')

    logo = models.ForeignKey(FileAttachment, on_delete=models.CASCADE, related_name='entitats', blank=True, null=True)

    codi_registre = models.CharField(max_length=256, blank=True, null=True, default='')
    password_default = models.CharField(max_length=256, blank=True, null=True, default='AMPA00')

    likable_issues = models.BooleanField(default=False)