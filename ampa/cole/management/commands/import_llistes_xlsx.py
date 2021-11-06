from django.core.management.base import BaseCommand
from django.db.models.functions import Concat
from django.db.models import Value as V

from cole.models import *

import unidecode
import pandas
import re

class Command(BaseCommand):
  help = 'Import llistes cole'

  def add_arguments(self, parser):
    parser.add_argument('file', nargs='+', type=str)
    parser.add_argument('--dry-run', action='store_true')


  def handle(self, *args, **options):
    try:
        dry_run = options['dry_run']
    except:
        dry_run = False

    filename = options['file'][0]

    admin_user = User.objects.filter(is_superuser=True).first()

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

    curs = Curs.objects.filter(modalitat=None).order_by('-curs').first()

    if not curs:
      print("No curs found")
      return

    print("Curs: {}".format(curs))

    for sheet_name in all_sheets_excel.keys():
      print("Processing sheet {}".format(sheet_name))

      etapa = Etapa.objects.filter(nom__icontains=sheet_name.lower().strip()).first()

      if etapa is None:
        print("Skipping sheet {}".format(sheet_name))
        continue
      else:
        print("Important etapa {}".format(etapa))

      excel_data_df = pandas.read_excel(filename, sheet_name=sheet_name, )

      excel_data_df.columns = [ "classe", "alumne" ]

      current_classe = ""
      for index, row in excel_data_df.iterrows():
        if type(row['classe']) == str and row['classe']:
          print("== "+row['classe']+' '+sheet_name)
          current_classe = row['classe']

          print("== "+current_classe[:-1]+'/'+current_classe[-1])
          existing_classe = Classe.objects.filter(nom__startswith=current_classe[:-1], nom__contains=current_classe[-1], curs=curs).first()

          if existing_classe:
            print("Found classe {} for {}".format(existing_classe, current_classe))
          else:
            print("Creating classe {}".format(current_classe))
            if not dry_run:
              new_classe = Classe(nom=row['classe'], curs=curs, etapa=etapa, delegat=admin_user)
              new_classe.save()

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
            cognoms = nom_filtered_alumne_parts[0].split(' ')
            if len(cognoms) == 1:
              cognom1 = cognoms[0]
              cognom2 = ''
            elif len(cognoms) == 2:
              cognom1 = cognoms[0]
              cognom2 = cognoms[1]
            else:
              cognom1 = cognoms[0]
              cognom2 = ' '.join(cognoms[1:])

            print("New student: "+nom_filtered_alumne_parts[1].strip()+'/'+cognom1+'/'+cognom2)

            if not dry_run:
              alumne = Alumne(nom=nom_filtered_alumne_parts[1].strip(), cognom1=cognom1, cognom2=cognom2)
              alumne.save()
              if existing_classe:
                alumne.classes.add(existing_classe)
              else:
                alumne.classes.add(new_classe)
              alumne.save()

          elif len(alumnes) == 1:
            

            if existing_classe:
              if existing_classe.alumnes.filter(pk=alumnes[0].pk).count() != 0:
                print("Alumne {} already in classe {}".format(alumnes[0], existing_classe))
                continue
                
            print("Promoting student: "+alumnes[0].print_name)
            if not dry_run:
              if existing_classe:
                alumnes[0].classes.add(existing_classe)
              else:
                alumnes[0].classes.add(new_classe)
              alumnes[0].save()

          else:
            print("Skipping due to multiple matches")
            for alumne in alumnes:
              print(" ? "+alumne.print_name)


