from django.db.models import Count
from django.db import models

from voting.models import *
from cole.models import *

import uuid

ISSUE_STATUS_DRAFT = 'a'
ISSUE_STATUS_OPEN = 'g'
ISSUE_STATUS_WAITING = 'p'
ISSUE_STATUS_CLOSED = 'z'
ISSUE_STATUS = [
    (ISSUE_STATUS_DRAFT, 'esborrany'),
    (ISSUE_STATUS_OPEN, 'proposada a junta'),
    (ISSUE_STATUS_WAITING, 'esperant resposta'),
    (ISSUE_STATUS_CLOSED, 'tancada'),
]

class Representant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, unique=True)
    ordre = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordre']
        indexes = [
            models.Index(fields=['ordre']),
        ]

class Issue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='issues', default=None, blank=True, null=True)
    representant = models.ForeignKey(Representant, on_delete=models.SET_NULL, related_name='issues', default=None, blank=True, null=True)

    titol = models.CharField(max_length=256)
    html_message = models.TextField(max_length=50000, default=None, blank=True, null=True)

    public = models.BooleanField(default=True)

    status = models.CharField(
        max_length=1,
        choices=ISSUE_STATUS,
        default=ISSUE_STATUS_DRAFT,
    )

    categories = models.ManyToManyField(Category, related_name='issues')

    likes = models.ManyToManyField(User, related_name='liked_issues')
    dislikes = models.ManyToManyField(User, related_name='disliked_issues')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def display_categories(self):
        return ','.join(list(self.categories.values_list('name', flat=True)))

    def display_juntes(self):
        return ','.join(list(self.juntes.values_list('name', flat=True)))

    def display_updated(self):
        updated = self.updated_at
        for comment in self.comments.all():
            if comment.updated_at > updated:
                updated = comment.updated_at
        return updated

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
        ]

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, related_name='comments', default=None, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', default=None, blank=True, null=True)
    representant = models.ForeignKey(Representant, on_delete=models.SET_NULL, related_name='comments', default=None, blank=True, null=True)

    html_message = models.TextField(max_length=50000, default=None, blank=True, null=True)

    internal = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

class Junta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    html_message = models.TextField(max_length=50000, default='', blank=True, null=True)

    public = models.BooleanField(default=False)

    celebracio = models.DateTimeField(default=None, blank=True, null=True)

    issues = models.ManyToManyField(Issue, related_name='juntes')
    votacions = models.ManyToManyField(Election, related_name='juntes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def _get_categories(self):
        return Category.objects.filter(id__in=self.issues.values('categories').distinct()).annotate(cat_count=Count('issues')).filter(cat_count__gt=1).order_by('ordre')

    categories = property(_get_categories)

    def _get_uncategorized_issues(self):
        return self.issues.filter(categories=None)

    uncategorized_issues = property(_get_uncategorized_issues)

    def _get_multicategorized_issues(self):
        return self.issues.annotate(cat_count=Count('categories')).filter(cat_count__gt=1)

    multicategorized_issues = property(_get_multicategorized_issues)


    class Meta:
        ordering = ['-celebracio']
        indexes = [
            models.Index(fields=['-celebracio']),
        ]