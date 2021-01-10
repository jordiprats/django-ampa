from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from cole.forms import *

import sys
import os

@user_passes_test(lambda u: u.is_staff)
def list_etapes(request):
    etapes = Etapa.objects.all()

    return render(request, 'etapes/list.html', {'etapes': etapes })

@user_passes_test(lambda u: u.is_staff)
def show_etapa(request, etapa_id):
    try:
        etapa_instance = Etapa.objects.filter(id=etapa_id)[0]

        return render(request, 'etapes/show.html', { 'content': 'overview', 'etapa_instance': etapa_instance, 'list_classes': etapa_instance.classes.all })
    except Exception as e:
        if request.user.is_staff:
            print(str(e))
            messages.error(request, str(e))
        return redirect('staff.settings')

@user_passes_test(lambda u: u.is_staff)
def edit_etapa(request, etapa_id=None):
    try:
        if etapa_id:
            new_etapa = False
            etapa_instance = Etapa.objects.filter(id=etapa_id)[0]
        else:
            new_etapa = True
            etapa_instance = Etapa()
        if request.method == 'POST':
            form = EtapaForm(request.POST, instance=etapa_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'etapes/edit.html', { 'form': form, 'etapa_instance': etapa_instance, 'new_etapa': new_etapa })
            return redirect('show.etapa', etapa_id=etapa_instance.id)
        else:
            form = EtapaForm(instance=etapa_instance)
        return render(request, 'etapes/edit.html', { 'form': form, 'etapa_instance': etapa_instance, 'new_etapa': new_etapa })
    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        if etapa_id:
            return redirect('show.etapa', etapa_id=etapa_id)
        else:
            return redirect('staff.settings')

#
# mailing
#

@user_passes_test(lambda u: u.is_staff)
def list_etapa_mailings(request, etapa_id):
    try:
        etapa_instance = Etapa.objects.filter(id=etapa_id).first()

        list_mailings = Mailing.objects.filter(etapa__id=etapa_id)

        return render(request, 'mailing/etapes/list.html', { 'etapa_instance': etapa_instance, 'list_mailings': list_mailings, 'content': 'mailing' })
    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        return redirect('show.etapa', etapa_id=etapa_id)


@user_passes_test(lambda u: u.is_staff)
def edit_mailing_etapa(request, etapa_id, mailing_id=None):
    try:
        instance_etapa = Etapa.objects.filter(id=etapa_id)[0]
        
        if mailing_id:
            instance_mailing = Mailing.objects.filter(etapa__id=instance_etapa.id, id=mailing_id)[0]
        else:
            instance_mailing = Mailing(etapa=instance_etapa, email_from='', email_reply_to=request.user.email)

        if request.method == 'POST':
            form = ClasseMailingForm(request.POST, instance=instance_mailing)
            if form.is_valid():
                form.save()
                messages.info(request, 'Guardat mailing')

                try:
                    boto_apretat = str(form.data['guardar'])
                    return redirect('list.etapa.mailings', etapa_id=etapa_id)
                except:
                    return redirect('add.attachment.mailing', mailing_id=instance_mailing.id)
                
            else:
                return render(request, 'mailing/etapes/edit.html', { 
                                                                        'form': form, 
                                                                        'instance_mailing': instance_mailing, 
                                                                        'image_hash': instance_mailing.images_hash,
                                                                        'attachment_hash': instance_mailing.attachment_hash
                                                                    })
            return redirect('list.etapa.mailings', etapa_id=etapa_id)
        else:
            form = ClasseMailingForm(instance=instance_mailing)
        return render(request, 'mailing/classes/edit.html', { 
                                                                'form': form, 
                                                                'instance_mailing': instance_mailing, 
                                                                'image_hash': instance_mailing.images_hash,
                                                                'attachment_hash': instance_mailing.attachment_hash
                                                            })

    except Exception as e:
        if settings.DEBUG:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        return redirect('list.etapa.mailings', etapa_id=etapa_id)

@user_passes_test(lambda u: u.is_staff)
def show_mailing_etapa(request, etapa_id, mailing_id):
    try:
        instance_etapa = Etapa.objects.filter(id=etapa_id)[0]
        
        instance_mailing = Mailing.objects.filter(etapa__id=etapa_id)[0]
        
        return render(request, 'mailing/classes/show.html', { 
                                                                'instance_mailing': instance_mailing, 
                                                                'instance_etapa': instance_etapa,
                                                                'image_hash': instance_mailing.images_hash,
                                                                'attachment_hash': instance_mailing.attachment_hash
                                                            })

    except Exception as e:
        if settings.DEBUG:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        return redirect('list.etapa.mailings', etapa_id=etapa_id)

# TODO:
@user_passes_test(lambda u: u.is_staff)
def enviar_mailing_etapa(request, classe_id, mailing_id):
    try:
        if request.user.is_superuser:
            instance_classe = Classe.objects.filter(id=classe_id)[0]
        else:
            instance_classe = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]
        
        instance_mailing = Mailing.objects.filter(classes__id=instance_classe.id)[0]
        
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                instance_mailing.status = MAILING_STATUS_PROGRAMAT
                instance_mailing.save()
                messages.info(request, 'e-Mail programat per enviar-se')

                return redirect('list.classe.mailings', classe_id=instance_classe.id)
            else:
                messages.error(request, 'Error eliminant l\'alumne')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'mailing/classes/enviar.html', { 'instance_mailing': instance_mailing, 'instance_classe': instance_classe })

    except Exception as e:
        print(str(e))
        return redirect('show.classe', classe_id=classe_id)