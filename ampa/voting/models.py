from django.db import models

from cole.models import *

import json

ELECTION_STATUS_DRAFT = '0'
ELECTION_STATUS_OPEN = '1'
ELECTION_STATUS_CLOSED = '2'
ELECTION_STATUS = [
    (ELECTION_STATUS_DRAFT, 'borrador'),
    (ELECTION_STATUS_OPEN, 'obertes'),
    (ELECTION_STATUS_CLOSED, 'tancades'),
]

class Election(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='elections', default=None, blank=True, null=True)

    multianswer = models.BooleanField(default=False)
    anonymous = models.BooleanField(default=False)

    titol = models.CharField(max_length=256)
    html_message = models.TextField(max_length=10000, default=None, blank=True, null=True)

    status = models.CharField(
        max_length=1,
        choices=ELECTION_STATUS,
        default=ELECTION_STATUS_DRAFT,
    )

    open_id = models.UUIDField(primary_key=False, default=None, editable=False, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_vote_count(self):
        total = 0
        for option in Vote.objects.filter(valid=True, election=self):
            total += 1
        return total

    def save(self, *args, **kwargs):
        if not self.open_id and self.status==ELECTION_STATUS_OPEN:
            self.open_id = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_at']

class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='options')
    
    text = models.CharField(max_length=1000, default='')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

##########################################################################################################################################

class ElectionLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='logs', blank=False, null=False)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='logs', blank=True, null=True)
    log = models.CharField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

##########################################################################################################################################

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes', blank=False, null=False)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='votes', blank=True, null=True)

    voter_id = models.CharField(max_length=256, default='', blank=True, null=True)
    voter_verification = models.CharField(max_length=256, default='', blank=True, null=True)

    valid = models.BooleanField(default=True)
    invalidation_reason = models.CharField(max_length=256, default='', blank=True, null=True)

    election_log = models.ForeignKey(ElectionLog, on_delete=models.CASCADE, related_name='votes', blank=True, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.election.status!=ELECTION_STATUS_OPEN:
            raise Exception('Vot no comptabilitzat')
        if self.option:
            log = ElectionLog(
                                election=self.election,
                                option=self.option, 
                                log=json.dumps( {
                                                    'id': str(self.id),
                                                    'voter_id': str(self.voter_id),
                                                    'voter_verification': str(self.voter_verification),
                                                    'election_id': str(self.election.id),
                                                    'option_id': str(self.option.id)
                                                })
                            )
        else:
            log = ElectionLog(
                                election=self.election,
                                option=None, 
                                log=json.dumps( {
                                                    'id': str(self.id),
                                                    'voter_id': str(self.voter_id),
                                                    'voter_verification': str(self.voter_verification),
                                                    'election_id': str(self.election.id),
                                                    'option_id': 'blanc'
                                                })
                            )
        log.save()
        self.election_log = log
        super().save(*args, **kwargs)