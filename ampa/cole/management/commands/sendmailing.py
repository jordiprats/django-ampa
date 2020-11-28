from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from cole.models import *

import html2text
import datetime
import pandas
import magic
import sys
import os
import re

class Command(BaseCommand):
    help = 'send emails'
    
    def add_arguments(self, parser):
        parser.add_argument('alumne_id', nargs='?', default=None)
        parser.add_argument('--email', nargs='?', default=None)

    # funció genèrica de emails
    def send_html_email(self, subject, html_message, email_from, email_reply_to, recipient_list, attachments={}):

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_message = text_maker.handle(html_message)

        if email_reply_to:
            headers = { 'Reply-To': email_reply_to }
        else:
            headers = {}

        # send_mail(subject=subject, message=text_email, from_email=email_from, recipient_list=recipient_list, html_message=html_message, headers=headers)

        mail = EmailMultiAlternatives(subject, text_message, email_from, recipient_list, headers=headers)
        mail.attach_alternative(html_message, 'text/html')

        for key in attachments:
            mime = magic.Magic(mime=True)
            mimetype = mime.from_file(attachments[key])
            
            attachment_fd = open(attachments[key], 'rb')
            mail.attach(key, attachment_fd.read(), mimetype)

        return mail.send()

    # cessió de dades
    def send_email_cessio_dades_alumne(self, alumne, to=None):
        if to:
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", to.lower())
        else:
            emails = alumne.emails
        
        headers = { 'Reply-To': alumne.classe.delegat.email }

        subject = 'Revisió dades AMPA - '+alumne.classe.nom
        html_message = '<html><body>Hola,<br>Des de l\'AMPA em demanen si podeu revisar les dades del vostre fill i donar el consentiment als delegats per fer-les servir per contactar amb vosaltres per temes del cole:<br><br><a href="http://ampa.systemadmin.es/alumnes/'+str(alumne.id)+'">http://ampa.systemadmin.es/alumnes/'+str(alumne.id)+'</a><br><br>Cal marcar la opció de cessió de dades per cada un dels pares, si voleu, rectificar si hi ha alguna dada incorrecte i al final hi ha també la opció per confirmar que les dades són correctes<br><br>Si us plau, no contesteu a aquest email, per qualsevol dubte contacteu amb el vostre delegat pels canals habituals<br><br>salutacions,</body></html>'
        email_from = settings.AMPA_DEFAULT_FROM
        recipient_list = emails

        self.send_html_email(subject, html_message, email_from, alumne.classe.delegat.email, recipient_list)       

    def handle(self, *args, **options):
        if options['alumne_id']:
            try:
                print(options['alumne_id'])
                alumne = Alumne.objects.filter(id=options['alumne_id'])[0]
                self.send_email_cessio_dades_alumne(alumne, options['email'])
            except Exception as e:
                print(str(e))
                print('Error enviament')
                return False           
        else:
            # mailing programats
            for mailing in Mailing.objects.filter(status=MAILING_STATUS_PROGRAMAT):
                if settings.DEBUG:
                    print(mailing.subject)

                if mailing.email_from:
                    email_from = mailing.email_from
                else:
                    email_from = settings.AMPA_DEFAULT_FROM

                if mailing.email_reply_to:
                    email_reply_to = mailing.email_reply_to
                else:
                    email_reply_to = None

                mailing_attachments = mailing.localfile_attachment_hash

                if settings.DEBUG:
                    print(str(mailing_attachments))

                for email in mailing.recipient_list:
                    if settings.DEBUG:
                        print(email)

                    footer_html = '<br><br>Per gestionar les comunicacions que voleu rebre:<br>'
                    for manual_unsubscribe_link in mailing.get_manual_unsubscribe_links(email):
                        footer_html += '<a href="'+settings.PUBLIC_DOMAIN+manual_unsubscribe_link+'">'+settings.PUBLIC_DOMAIN+manual_unsubscribe_link+'</a><br>'

                    try:
                        self.send_html_email(
                                                subject=mailing.subject, 
                                                html_message=mailing.html_message+footer_html,
                                                email_from=email_from,
                                                email_reply_to=email_reply_to,
                                                recipient_list= [ email ],
                                                attachments=mailing_attachments
                                            )
                    except Exception as e:
                        if settings.DEBUG:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno)
                            print(str(e))

                mailing.status = MAILING_STATUS_ENVIAT
                mailing.save()
            # cessió de dades
            for classe in Classe.objects.filter(ready_to_send=True, ultim_email=None):
                try:
                    print("classe: "+classe.nom)
                    for alumne in classe.alumnes.all():
                        if alumne.emails:
                            self.send_email_cessio_dades_alumne(alumne)
                    classe.ready_to_send = False
                    classe.ultim_email = datetime.datetime.now()
                    classe.save()
                except Exception as e:
                    classe.ready_to_send = False
                    classe.save()
                    if settings.DEBUG:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(str(e))