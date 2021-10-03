from django.core.management.base import BaseCommand
from django.db.models.functions import Concat
from django.db.models import Value as V

from cole.models import *

class Command(BaseCommand):
  help = 'Cleanup Alumnes sense classes'

  def handle(self, *args, **options):
    filename = options['file'][0]

    for alumne in Alumne.objects.filter(classes=None):
      print("Deleting alumne {}".format(alumne._get_print_name()))
      alumne.delete()

    for alumne in Alumne.objects.all():
      if alumne.classes.count() == 0:
        print("Deleting alumne {}".format(alumne._get_print_name()))
        alumne.delete()
      else:
        alumne.save()

