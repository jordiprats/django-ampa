from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from cole.models import *

import xlsxwriter
import pathlib
import random
import pandas
import sys
import os
import re

class Command(BaseCommand):
    help = 'Import uploaded XLS files'

    def add_arguments(self, parser):
        parser.add_argument('classe_id', nargs='?', default=None)
        parser.add_argument('--output', nargs='?', default=None)

    def handle(self, *args, **options):
        if options['classe_id']:
            try:
                classe_instance = Classe.objects.filter(id=options['classe_id'])[0]
            except:
                print('Class no trobada')
                return False
        else:
            try:
                classe_instance = Classe.objects.filter(waiting_export=True)[0]
            except:
                # print('Res a procesar')
                return False

        if options['output']:
            output_file = options['output']
        else:
            characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            random_id = ''

            for i in range(0, 6):
                random_id += random.choice(characters)

            output_file_name = random_id+'_'+classe_instance.nom+'.xlsx'
            output_file = os.path.join(settings.XLS_ROOT, 'export/', output_file_name)
            print(output_file)
            pathlib.Path(os.path.join(settings.XLS_ROOT, 'export/')).mkdir(parents=True, exist_ok=True)

        try:
            workbook = xlsxwriter.Workbook(output_file)
            worksheet = workbook.add_worksheet('Fulla 1')

            # Tamany columnes
            worksheet.set_column('B:D', 10)
            worksheet.set_column('E:J', 10)
            worksheet.set_column('L:L', 30)
            worksheet.set_column('M:M', 40)

            # Formats
            text_normal = workbook.add_format({ 'font_size': 9 })
            text_destacat = workbook.add_format({ 'font_size': 14 })
            text_normal_taula = workbook.add_format({ 'font_size': 9, 'border': 1 })
            text_normal_taula_centre = workbook.add_format({ 'font_size': 9, 'border': 1, 'align': 'center' })
            text_normal_taula_bg_vermell = workbook.add_format({ 'font_size': 9, 'bg_color': '#FFC7CE', 'border': 1 })
            text_normal_centre = workbook.add_format({ 'font_size': 9, 'align': 'center' })
            data_normal = workbook.add_format({ 'font_size': 9, 'num_format': 'dd/mm/yy' })
            data_normal_taula = workbook.add_format({ 'font_size': 9, 'num_format': 'dd/mm/yy', 'border': 1 })
            bold = workbook.add_format({ 'bold': True, 'font_size': 9 })
            bold_destacat = workbook.add_format({ 'bold': True, 'font_size': 14 })
            bold_taula = workbook.add_format({ 'bold': True, 'font_size': 9, 'border': 1 })
            bold_taula_centre = workbook.add_format({ 'bold': True, 'font_size': 9, 'border': 1, 'align': 'center' })
            bold_center = workbook.add_format({ 'bold': True, 'font_size': 9, 'align': 'center' })

            worksheet.write('A1', 'CLASSE:', bold)
            worksheet.write('B1', classe_instance.nom, bold_destacat)

            worksheet.write('A3', 'TUTOR:', bold)
            worksheet.write('B3', classe_instance.tutor, text_normal)

            worksheet.write('E1', 'DELEGAT:', bold)
            worksheet.write('F1', classe_instance.nom_delegat, text_normal)
            worksheet.write('H1', 'Telèfon:', bold)
            worksheet.write('I1', classe_instance.telefon_delegat, text_normal)
            worksheet.write('K1', 'e-Mail:', bold)
            worksheet.write('L1', classe_instance.email_delegat, text_normal)

            worksheet.insert_image('M1', os.path.join(settings.STATIC_FULLPATH, 'logo_cole.jpg'), {'x_scale': 0.34, 'y_scale': 0.34})
            
            worksheet.write('E3', 'SUBDELEGAT:', bold)
            worksheet.write('F3', classe_instance.nom_subdelegat, text_normal)
            worksheet.write('H3', 'Telèfon:', bold)
            worksheet.write('I3', classe_instance.telefon_subdelegat, text_normal)
            worksheet.write('K3', 'e-Mail:', bold)
            worksheet.write('L3', classe_instance.email_subdelegat, text_normal)

            # M1 imatge AMPA
            worksheet.write('M5', 'Associació de Mapes i Pares del Col·legi', bold_center)
            worksheet.write('M6', 'Lestonnac de Barcelona', bold_center)

            header = {
                'A': '',
                'B': 'Nom',
                'C': 'Primer Cognom',
                'D': 'Segon Cognom',
                'E': 'Data de naixement',
                'F': 'Tutor 1',
                'G': 'Telèfon',
                'H': 'Cessió de dades *',
                'I': 'Tutor 2',
                'J': 'Telèfon',
                'K': 'Cessió de dades *',
                'L': 'e-Mails',
                'M': 'Ús responsable de les dades ** (signatura)',
            }

            for item in header:
                worksheet.write(item+'7', header[item], bold_taula)

            worksheet.merge_range('C7:D7', 'Cognom', bold_taula_centre)

            linea = 8
            for alumne in classe_instance.alumnes.order_by('num_llista').all():
                worksheet.write('A'+str(linea), alumne.num_llista, text_normal_taula)
                worksheet.write('B'+str(linea), alumne.nom, text_normal_taula)
                worksheet.write('C'+str(linea), alumne.cognom1, text_normal_taula)
                worksheet.write('D'+str(linea), alumne.cognom2, text_normal_taula)

                if alumne.naixement:
                    worksheet.write('E'+str(linea), alumne.naixement.replace(tzinfo=None), data_normal_taula)
                else:
                     worksheet.write('E'+str(linea), '', text_normal_taula)

                worksheet.write('F'+str(linea), alumne.tutor1, text_normal_taula)
                worksheet.write('G'+str(linea), alumne.telf_tutor1, text_normal_taula)
                if alumne.tutor1_cessio:
                    worksheet.write('H'+str(linea), 'SI', text_normal_taula)
                else:
                    worksheet.write('H'+str(linea), 'NO', text_normal_taula_bg_vermell)

                worksheet.write('I'+str(linea), alumne.tutor2, text_normal_taula)
                worksheet.write('J'+str(linea), alumne.telf_tutor2, text_normal_taula)
                if alumne.tutor2_cessio:
                    worksheet.write('K'+str(linea), 'SI', text_normal_taula)
                else:
                    worksheet.write('K'+str(linea), 'NO', text_normal_taula_bg_vermell)

                worksheet.write('L'+str(linea), alumne.emails, text_normal_taula)

                if alumne.validat:
                    worksheet.write('M'+str(linea), 'SI', text_normal_taula)
                else:
                    worksheet.write('M'+str(linea), 'NO', text_normal_taula_bg_vermell)
                linea += 1

            linea += 1

            worksheet.write('A'+str(linea), 'Les dades incloses en aquest document podran ser incorporades a un fitxer de dades personals amb la finalitat de gestionar les relacions entre l\'AMPA Lestonnac i les famílies. ', text_normal)
            linea += 1
            worksheet.write('A'+str(linea), 'L\'AMPA Lestonnac utilitzarà aquestes dades per aquelles activitats que li siguin pròpies i no les cedirà a terceres persones o organismes, tret de les autoritzades al document, sense la seva autiorització expressa.', text_normal)
            linea += 1            
            worksheet.write('A'+str(linea), 'En aplicació de la LO 15/1999 i del RD 1332/1994 vostè podrà exercir el seu dret d\'accés, rectificació o cancel·lació d\'aquestes dades a la Secretaria de l\'AMPA.', text_normal)

            linea +=2

            worksheet.write('A'+str(linea), '*', text_normal_centre)
            worksheet.write('B'+str(linea), 'Si accepta que aquestes dades es facilitin al delegat i al grup classe marqui la casella corresponent', text_normal_centre)
            linea += 1
            worksheet.write('A'+str(linea), '**', text_normal_centre)
            worksheet.write('B'+str(linea), 'Accepta fer un ús responsable i no facilitar a tercers les dades del grup classe que proporcionarà el delegat de classe ', text_normal_centre)



            workbook.close()           
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        if not options['output']:
            classe_instance.latest_export = output_file_name
            classe_instance.waiting_export = False
            classe_instance.save()
