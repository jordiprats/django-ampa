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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.open_id and self.status==ELECTION_STATUS_OPEN:
            self.open_id = uuid.uuid4

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

    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='logs')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='logs')
    log = models.CharField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

##########################################################################################################################################

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='votes')

    voter_id = models.CharField(max_length=256, default='')
    voter_verification = models.CharField(max_length=256, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.option.election.status!=ELECTION_STATUS_OPEN:
            raise Exception('Vot no comptabilitzat')
        super().save(*args, **kwargs)
        #log = ElectionLog(option=self.option, log=str(self.id)+'@'+self.voter_id+'#'+self.voter_verification+'~'+str(self.question.id)+'!'+str(self.option.id))
        log = ElectionLog(
                            option=self.option, 
                            log=json.dumps( {
                                                'id': self.id,
                                                'voter_id': self.voter_id,
                                                'voter_verification': self.voter_verification,
                                                'election_id': self.option.election.id,
                                                'option_id': self.option.id
                                            })
                        )
        log.save()