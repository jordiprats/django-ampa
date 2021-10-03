from django.core.management.base import BaseCommand
from django.db.models.functions import Concat
from django.db.models import Value as V

from cole.models import *

import unidecode
import pandas
import re

class Command(BaseCommand):
  help = 'Import uploaded XLS files'

  def add_arguments(self, parser):
    parser.add_argument('file', nargs='+', type=str)

  def handle(self, *args, **options):
    filename = options['file'][0]

    for alumne in Alumne.objects.filter(classes=None):
      print("Deleting alumne {}".format(alumne._get_print_name()))
      #alumne.delete()

    for alumne in Alumne.objects.all():
      if alumne.classes.count() == 0:
        print("Deleting alumne {}".format(alumne._get_print_name()))
        alumne.delete()
      else:
        alumne.save()

    all_sheets_excel = pandas.read_excel(filename, sheet_name=None, )

    for sheet_name in all_sheets_excel.keys():
      excel_data_df = pandas.read_excel(filename, sheet_name=sheet_name, )

      excel_data_df.columns = [ "classe", "alumne" ]

      current_classe = ""
      for index, row in excel_data_df.iterrows():
        if type(row['classe']) == str and row['classe']:
          print("== "+row['classe']+' '+sheet_name)
          current_classe = row['classe']
          continue

        if type(row['alumne']) == str and row['alumne']:
          nom_filtered_alumne = re.sub(' +', ' ', row['alumne'].strip())
          nom_filtered_alumne = nom_filtered_alumne.replace('·', '.')
          nom_filtered_alumne = unidecode.unidecode(nom_filtered_alumne)
          nom_filtered_alumne = nom_filtered_alumne.lower()
          nom_filtered_alumne_parts = nom_filtered_alumne.split(',')
          nom_filtered_alumne = nom_filtered_alumne_parts[1].strip()+' '+nom_filtered_alumne_parts[0].strip()
          #nom_filtered_alumne = nom_filtered_alumne.replace(' ,', ',')
          # print("?="+nom_filtered_alumne)
          alumnes = Alumne.objects.annotate(full_name=Concat('nom_unaccented', V(' '), 'cognom1_unaccented', V(' '), 'cognom2_unaccented', )).filter(full_name__icontains=nom_filtered_alumne)
          if len(alumnes) == 0:
            print(" X? "+nom_filtered_alumne)
          elif len(alumnes) == 1:
            print("   "+alumnes[0].print_name)
          else:
            for alumne in alumnes:
              print(" ? "+alumne.print_name)


