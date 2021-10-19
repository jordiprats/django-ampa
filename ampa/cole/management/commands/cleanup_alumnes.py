from django.core.management.base import BaseCommand
from django.db.models.functions import Concat
from django.db.models import Value as V

from cole.models import *

class Command(BaseCommand):
  help = 'Cleanup Alumnes sense classes'

  def handle(self, *args, **options):
    
    # Alumnes sense classes
    for alumne in Alumne.objects.filter(classes=None):
      alumne.delete()

    # fem save de tots
    for alumne in Alumne.objects.all():
      if alumne.classes.count() == 0:
        alumne.delete()
      else:
        alumne.save()

