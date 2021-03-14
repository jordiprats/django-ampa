from django.core.management.base import BaseCommand, CommandError
from django_xhtml2pdf.utils import generate_pdf
from django.conf import settings
from peticions.models import *
from cole.models import *
from io import BytesIO

import pathlib
import random
import sys
import re
import os

class Command(BaseCommand):
    help = 'Export junta a PDF'

    def add_arguments(self, parser):
        parser.add_argument('junta_id', nargs='?', default=None)
        parser.add_argument('--output', nargs='?', default=None)

    def handle(self, *args, **options):
        if options['junta_id']:
            try:
                junta_instance = Junta.objects.filter(id=options['junta_id'])[0]
            except:
                print('Junta no trobada')
                return False
        else:
            try:
                junta_instance = Junta.objects.filter(public=True, latest_export=None)[0]
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

            output_file_name = random_id+'/'+junta_instance.slug+'.pdf'
            output_file = os.path.join(settings.XLS_ROOT, 'export/', output_file_name)
            print(output_file)
            pathlib.Path(os.path.join(settings.XLS_ROOT, 'export/')).mkdir(parents=True, exist_ok=True)

        try:
            output_fd = BytesIO()
            generate_pdf('peticions/juntes/render_pdf.html', file_object=output_fd, context={
                                                                            'junta_instance': junta_instance, 
                                                                            'issue_add_comments': False,
                                                                            'issue_title_size': 'h4',
                                                                            'user_admin': True,
                                                                            'is_pdf': True
                                                                        })
            with open(output_file, "wb") as f:
                f.write(output_fd.getbuffer())

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        


        if not options['output']:
            junta_instance.latest_export = output_file_name
            junta_instance.save()
