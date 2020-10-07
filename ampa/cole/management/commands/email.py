from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from cole.models import *

import pandas
import sys
import os
import re

class Command(BaseCommand):
    help = 'send emails'

    def add_arguments(self, parser):
        parser.add_argument('classe', nargs='+', type=str)
        parser.add_argument('curs', nargs='+', type=str)
    
    def handle(self, *args, **options):
        try:
            classe = Classe.objects.filter(nom=options['classe'][0], curs=options['curs'][0])[0]
        
            for alumne in classe.alumnes.all():
                emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", alumne.emails)
                for email in emails:
                    subject = 'Revisió dades AMPA - '+options['classe'][0]
                    message = 'Hola,\nDes de l\'AMPA em demanen si podeu revisar les dades del vostre fill i donar el consentiment als delegats per fer-les servir per contactar amb vosaltres per temes del cole:\n\nhttp://ffdsfsdfsd/'+str(alumne.id)+"\n\nCal marcar la opció de cessió de dades per cada un dels pares, si voleu, rectificar si hi ha alguna dada incorrecte i al final hi ha també la opció per confirmar que les dades són correctes\n\nsalutacions,"
                    html_message = '<html><body>Hola,<br>Des de l\'AMPA em demanen si podeu revisar les dades del vostre fill i donar el consentiment als delegats per fer-les servir per contactar amb vosaltres per temes del cole:<br><br><a href="http://ampa.systemadmin.es/alumnes/'+str(alumne.id)+'">http://ampa.systemadmin.es/alumnes/'+str(alumne.id)+'</a><br><br>Cal marcar la opció de cessió de dades per cada un dels pares, si voleu, rectificar si hi ha alguna dada incorrecte i al final hi ha també la opció per confirmar que les dades són correctes<br><br>salutacions,</body></html>'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [ email ]
                    send_mail( subject=subject, message=message, from_email=email_from, recipient_list=recipient_list, html_message=html_message)
                    # print('subject:' +subject)
                    # print('message:' +message)
                    # print('html_message:' +html_message)
                    # print('recipient_list:' +str(recipient_list))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))


