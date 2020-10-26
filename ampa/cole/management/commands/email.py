from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from cole.models import *

import datetime
import pandas
import sys
import os
import re

class Command(BaseCommand):
    help = 'send emails'
    
    def add_arguments(self, parser):
        parser.add_argument('alumne_id', nargs='?', default=None)
        parser.add_argument('--email', nargs='?', default=None)

    def send_email_alumne(self, alumne, to=None):
        if to:
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", to.lower())
        else:
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", alumne.emails.lower())
        
        subject = 'Revisió dades AMPA - '+alumne.classe.nom
        message = 'Hola,\nDes de l\'AMPA em demanen si podeu revisar les dades del vostre fill i donar el consentiment als delegats per fer-les servir per contactar amb vosaltres per temes del cole:\n\nhttp://ffdsfsdfsd/'+str(alumne.id)+"\n\nCal marcar la opció de cessió de dades per cada un dels pares, si voleu, rectificar si hi ha alguna dada incorrecte i al final hi ha també la opció per confirmar que les dades són correctes\n\nSi us plau, no contesteu a aquest email, per qualsevol dubte contacteu amb el vostre delegat pels canals habituals\n\nsalutacions,"
        html_message = '<html><body>Hola,<br>Des de l\'AMPA em demanen si podeu revisar les dades del vostre fill i donar el consentiment als delegats per fer-les servir per contactar amb vosaltres per temes del cole:<br><br><a href="http://ampa.systemadmin.es/alumnes/'+str(alumne.id)+'">http://ampa.systemadmin.es/alumnes/'+str(alumne.id)+'</a><br><br>Cal marcar la opció de cessió de dades per cada un dels pares, si voleu, rectificar si hi ha alguna dada incorrecte i al final hi ha també la opció per confirmar que les dades són correctes<br><br>Si us plau, no contesteu a aquest email, per qualsevol dubte contacteu amb el vostre delegat pels canals habituals<br><br>salutacions,</body></html>'
        email_from = 'Delegats Lestonnac <noreply@systemadmin.es>'
        recipient_list = emails

        send_mail( subject=subject, message=message, from_email=email_from, recipient_list=recipient_list, html_message=html_message)

    def handle(self, *args, **options):
        if options['alumne_id']:
            try:
                print(options['alumne_id'])
                alumne = Alumne.objects.filter(id=options['alumne_id'])[0]
                self.send_email_alumne(alumne, options['email'])
            except Exception as e:
                print(str(e))
                print('Error enviament')
                return False           
        else:
            for classe in Classe.objects.filter(ready_to_send=True, ultim_email=None):
                try:
                    print("classe: "+classe.nom)
                    for alumne in classe.alumnes.all():
                        if alumne.emails:
                            self.send_email_alumne(alumne)
                    classe.ready_to_send = False
                    classe.ultim_email = datetime.datetime.now()
                    classe.save()
                except Exception as e:
                    classe.ready_to_send = False
                    classe.save()
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(str(e))