from django.core.management.base import BaseCommand, CommandError
from cole.models import *

import pandas
import sys
import os
import re

class Command(BaseCommand):
    help = 'Import uploaded XLS files'

    def handle(self, *args, **options):
        for fileupload in FileUpload.objects.filter(processed=False).order_by('updated_at'):
            # excel_data_df = pandas.read_excel(fileupload.filepath, sheet_name='Hoja1', )

            try:
                all_sheets_excel = pandas.read_excel(fileupload.filepath, sheet_name=None, )
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(str(e))
                fileupload.error = True
                fileupload.processed = True
                fileupload.save()
                continue

            for sheet_name in all_sheets_excel.keys():
                try:
                    excel_data_df = pandas.read_excel(fileupload.filepath, sheet_name=sheet_name, )

                    excel_data_df = excel_data_df[6:]

                    excel_data_df.columns = [
                                    "id_nen",
                                    "nom",
                                    "cognom1",
                                    "cognom2",
                                    "naixement",
                                    "pare",
                                    "telf1",
                                    "mare",
                                    "telf2",
                                    "email",
                                    "cessio",
                                    "signatura"
                                ]

                    excel_data_df = excel_data_df.dropna(subset=['id_nen', 'nom', 'cognom1'])

                    excel_data_df = excel_data_df.where(pandas.notnull(excel_data_df), None)

                    # print whole sheet data
                    # print(excel_data_df)
                    for index, row in excel_data_df.iterrows():
                        if row['nom']:
                            stripped_nom = row['nom'].strip()
                        else:
                            stripped_nom = row['nom']

                        if row['cognom1']:
                            stripped_cognom1 = row['cognom1'].strip()
                        else:
                            stripped_cognom1 = row['cognom1']

                        if row['cognom2']:
                            stripped_cognom2 = row['cognom2'].strip()
                        else:
                            stripped_cognom2 = row['cognom2']

                        if type(row['naixement']) == str:
                            print("str: "+row['naixement'])
                            try:
                                parsed_naixement = datetime.datetime.strptime(row['naixement'], "%m/%d/%Y").date()
                            except:
                                try:
                                    parsed_naixement = datetime.datetime.strptime(row['naixement'], "%d/%m/%Y").date()
                                except:
                                    parsed_naixement = None
                        elif type(row['naixement']) == int:
                            parsed_naixement = None
                        else:
                            parsed_naixement = row['naixement']
                        try:
                            nou_alumne = Alumne.objects.filter(
                                                                nom = stripped_nom, 
                                                                cognom1 = stripped_cognom1, 
                                                                cognom2 = stripped_cognom2, 
                                                                num_llista = row['id_nen'],
                                                            )[0]
                        except IndexError:
                            try:
                                nou_alumne = Alumne(

                                    nom = stripped_nom, 
                                    cognom1 = stripped_cognom1, 
                                    cognom2 = stripped_cognom2, 
                                    num_llista = row['id_nen'],
                                    naixement = parsed_naixement,
                                
                                    tutor1 = row['pare'],
                                    telf_tutor1 = row['telf1'],
                                    tutor1_cessio = False,

                                    tutor2 = row['mare'],
                                    telf_tutor2 = row['telf2'],
                                    tutor2_cessio = False,

                                    email_tutor1 = row['email'],

                                    validat = False,
                                )
                            except:
                                print('DEBUG: '+str(row))
                                pass
                        if nou_alumne.nom:
                            nou_alumne.nom = nou_alumne.nom.strip()

                        if nou_alumne.cognom1:
                            nou_alumne.cognom1 = nou_alumne.cognom1.strip()

                        if nou_alumne.cognom2:
                            nou_alumne.cognom2 = nou_alumne.cognom2.strip()

                        if nou_alumne.tutor1:
                            nou_alumne.tutor1 = nou_alumne.tutor1.strip()

                        if nou_alumne.tutor2:
                            nou_alumne.tutor2 = nou_alumne.tutor2.strip()

                        nou_alumne.classes.add(fileupload.classe)

                        nou_alumne.save()

                        print(str(nou_alumne))
                    fileupload.processed = True
                    fileupload.save()

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(str(e))
                    fileupload.error = True
                    fileupload.processed = True
                    fileupload.save()

