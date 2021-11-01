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
        parser.add_argument('--dry-run', action='store_true')

    # funció genèrica de emails
    def send_html_email(self, subject, html_message, email_from, email_reply_to, recipient_list, attachments={}, dry_run=False):

        print('Sending email to: '+str(recipient_list))
        print('Subject: '+subject)
        print('From: '+email_from)
        if email_reply_to:
            print('Reply-To: '+email_reply_to)
        print('Attachments: '+str(attachments))

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_message = text_maker.handle(html_message)

        if email_reply_to:
            headers = { 'Reply-To': email_reply_to }
        else:
            headers = {}
        
        print('Headers: '+str(headers))

        # send_mail(subject=subject, message=text_email, from_email=email_from, recipient_list=recipient_list, html_message=html_message, headers=headers)

        mail = EmailMultiAlternatives(subject, text_message, email_from, recipient_list, headers=headers)
        mail.attach_alternative(html_message, 'text/html')

        for key in attachments:
            mime = magic.Magic(mime=True)
            mimetype = mime.from_file(attachments[key])
            
            attachment_fd = open(attachments[key], 'rb')
            mail.attach(key, attachment_fd.read(), mimetype)

        if dry_run:
            print("enviant: "+str(recipient_list))
        else:
            return mail.send()

    # cessió de dades
    def send_email_cessio_dades_alumne(self, alumne, to=None, dry_run=False):
        if to:
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", to.lower())
        else:
            emails = alumne.cessio_emails

        print(str(emails))
        
        headers = { 'Reply-To': alumne.classe.delegat.email }

        subject = 'Revisió dades AMPA - '+alumne.classe.nom
        html_message = '<html><body>Hola,<br>Per tal de poder rebre comunicacions de l\'AMPA cal donar el consentiment a l\'AMPA i als delegats per fer servir les vostres dades per tal de contactar amb vosaltres per temes del cole:<br><br><a href="http://ampa.systemadmin.es/alumnes/'+str(alumne.id)+'">http://ampa.systemadmin.es/alumnes/'+str(alumne.id)+'</a><br><br>Cal marcar la opció de cessió de dades per cada un dels tutors<br><br>Si us plau, no contesteu a aquest email, per qualsevol dubte contacteu amb el vostre delegat pels canals habituals<br><br>Delegats '+alumne.classe.nom+' '+alumne.classe.etapa+',</body></html>'
        email_from = settings.AMPA_DEFAULT_FROM
        recipient_list = emails

        for email in recipient_list:
            print('Sending email to: '+email)
            self.send_html_email(subject=subject, html_message=html_message, email_from=email_from, email_reply_to=alumne.classe.delegat.email, recipient_list=[ email ], attachments={}, dry_run=dry_run)

    def handle(self, *args, **options):
        try:
            dry_run = options['dry_run']
        except:
            dry_run = False

        # TODO: locking for multi instance

        if options['alumne_id']:
            print('mailing '+options['alumne_id'])
            try:
                print(options['alumne_id'])
                alumne = Alumne.objects.filter(id=options['alumne_id'])[0]
                self.send_email_cessio_dades_alumne(alumne, options['email'])
            except Exception as e:
                print(str(e))
                print('Error enviament')
                return False           
        else:
            print('checking for mailings...')
            # mailing programats
            for mailing in Mailing.objects.filter(status=MAILING_STATUS_PROGRAMAT):
                print(mailing.subject)

                # if mailing.email_from:
                #     email_from = mailing.email_from
                # else:
                email_from = settings.AMPA_DEFAULT_FROM

                if mailing.email_reply_to:
                    email_reply_to = mailing.email_reply_to
                else:
                    email_reply_to = None

                mailing_attachments = mailing.localfile_attachment_hash

                print(str(mailing_attachments))

                if mailing.nomes_delegats:
                    destinataris = []
                    for classe in mailing.classes.all():
                        if classe.email_delegat:
                            destinataris += re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", classe.email_delegat.lower().strip())
                        if classe.email_subdelegat:
                            destinataris += re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", classe.email_subdelegat.lower().strip())
                else:
                    destinataris = mailing.recipient_list

                for each_email in destinataris:
                    print(each_email)

                    footer_html = '<br><br>Per gestionar les comunicacions que voleu rebre:<br>'
                    for manual_unsubscribe_link in mailing.get_manual_unsubscribe_links(each_email):
                        footer_html += '<a href="'+settings.PUBLIC_DOMAIN+manual_unsubscribe_link+'">'+settings.PUBLIC_DOMAIN+manual_unsubscribe_link+'</a><br>'

                    try:
                        # si el email ja l'haviem provat, skip
                        if EmailSent.objects.filter(mailing=mailing, email=each_email)[0]:
                            continue
                    except:
                        pass

                    email = EmailSent(mailing=mailing, email=each_email)
                    try:
                        self.send_html_email(
                                                subject=mailing.subject, 
                                                html_message=mailing.html_message+footer_html,
                                                email_from=email_from,
                                                email_reply_to=email_reply_to,
                                                recipient_list= [ each_email ],
                                                attachments=mailing_attachments,
                                                dry_run=dry_run
                                            )
                        email.sent = True
                    except Exception as e:
                        email.error = True
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

                        email.what = str(e)
                        email.where = str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno)
                        email.error = True

                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(str(e))
                    email.save()

                mailing.status = MAILING_STATUS_ENVIAT
                mailing.save()
            
            # cessió de dades
            print('checking for cessió de dades...')

            for classe in Classe.objects.filter(ready_to_send=True, ultim_email=None):
                print("classe: "+classe.nom+" "+classe.etapa+" "+classe.curs)
                try:
                    for alumne in classe.alumnes.all():
                        self.send_email_cessio_dades_alumne(alumne, dry_run=dry_run)
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