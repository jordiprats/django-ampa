from django.db import models

from voting.models import *
from cole.models import *


ISSUE_STATUS_DRAFT = 'a'
ISSUE_STATUS_OPEN = 'g'
ISSUE_STATUS_WAITING = 'p'
ISSUE_STATUS_CLOSED = 'z'
ISSUE_STATUS = [
    (ISSUE_STATUS_DRAFT, 'borrador'),
    (ISSUE_STATUS_OPEN, 'obert'),
    (ISSUE_STATUS_WAITING, 'pendent'),
    (ISSUE_STATUS_CLOSED, 'tancat'),
]

class Category(models.Model):
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

class Issue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='issues', default=None, blank=True, null=True)

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

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
        ]

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, related_name='comments', default=None, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', default=None, blank=True, null=True)

    html_message = models.TextField(max_length=50000, default=None, blank=True, null=True)

    internal = models.BooleanField(default=False)

    ampa = models.BooleanField(default=False)

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

    class Meta:
        ordering = ['-celebracio']
        indexes = [
            models.Index(fields=['-celebracio']),
        ]