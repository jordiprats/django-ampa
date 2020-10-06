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
    email = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username, allow_unicode=False)
        super().save(*args, **kwargs)

class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nom = models.CharField(max_length=256)

    delegat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delegatsclasses')
    subdelegat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subdelegatsclasses')

class Alumne(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #id_nen         nom        cognom1     cognom2            naixement         pare      telf1       mare      telf2                                              email     cessio signatura
    num_llista = models.IntegerField()
    nom = models.CharField(max_length=256)
    cognom1 = models.CharField(max_length=256)
    cognom2 = models.CharField(max_length=256, default='', blank=True)
    naixement = models.DateTimeField()
    tutor1 = models.CharField(max_length=256, default='', blank=True)
    telf_tutor1 = models.CharField(max_length=256, default='', blank=True)
    tutor2 = models.CharField(max_length=256, default='', blank=True)
    telf_tutor2 = models.CharField(max_length=256, default='', blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    classe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alumnes')

    class Meta:
        unique_together = ('num_llista', 'nom', 'cognom1', 'cognom2')
        ordering = ['-num_llista']
        indexes = [
            models.Index(fields=['-num_llista',]),
        ]


class FileUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owners = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='uploads')

    processed = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at',]),
        ]
