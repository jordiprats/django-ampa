from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from cole.forms import *

import sys
import os

@user_passes_test(lambda u: u.is_staff)
def list_cursos(request):
    cursos = Curs.objects.all()

    return render(request, 'cursos/list.html', {'cursos': cursos })

@user_passes_test(lambda u: u.is_staff)
def show_curs(request, curs_id):
    try:
        curs_instance = Curs.objects.filter(id=curs_id)[0]

        return render(request, 'cursos/show.html', { 'content': 'overview', 'curs_instance': curs_instance, 'list_classes': curs_instance.classes.all() })
    except Exception as e:
        if request.user.is_staff:
            print(str(e))
            messages.error(request, str(e))
        return redirect('staff.settings')

@user_passes_test(lambda u: u.is_staff)
def edit_curs(request, curs_id=None):
    try:
        if curs_id:
            new_curs = False
            curs_instance = Curs.objects.filter(id=curs_id)[0]
            print("caca "+str(curs_instance.modalitat))
        else:
            new_curs = True
            curs_instance = Curs()
        if request.method == 'POST':
            form = CursForm(request.POST, instance=curs_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'cursos/edit.html', { 'form': form, 'curs_instance': curs_instance, 'new_curs': new_curs })
            return redirect('show.curs', curs_id=curs_instance.id)
        else:
            form = CursForm(instance=curs_instance)
        return render(request, 'cursos/edit.html', { 'form': form, 'curs_instance': curs_instance, 'new_curs': new_curs })
    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        if curs_id:
            return redirect('show.curs', curs_id=curs_id)
        else:
            return redirect('staff.settings')

#
# mailing
#

@user_passes_test(lambda u: u.is_staff)
def list_curs_mailings(request, curs_id):
    try:
        curs_instance = Curs.objects.filter(id=curs_id, modalitat=None).first()

        list_mailings = Mailing.objects.filter(curs__id=curs_id)

        return render(request, 'mailing/cursos/list.html', { 'curs_instance': curs_instance, 'list_mailings': list_mailings, 'content': 'mailing' })
    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        return redirect('show.curs', curs_id=curs_id)

@user_passes_test(lambda u: u.is_staff)
def edit_mailing_curs(request, curs_id, mailing_id=None):
    try:
        instance_curs = Curs.objects.filter(id=curs_id)[0]
        
        if mailing_id:
            instance_mailing = Mailing.objects.filter(curs__id=instance_curs.id, id=mailing_id)[0]
        else:
            instance_mailing = Mailing(curs=instance_curs, email_from=None, email_reply_to=None)

        if request.method == 'POST':
            if request.user.is_staff:
                form = StaffMailingForm(request.POST, instance=instance_mailing)    
            else:
                form = UserMailingForm(request.POST, instance=instance_mailing)
            if form.is_valid():
                form.save()
                messages.info(request, 'Guardat mailing')

                try:
                    boto_apretat = str(form.data['guardar'])
                    return redirect('list.curs.mailings', curs_id=curs_id)
                except:
                    return redirect('add.attachment.mailing', mailing_id=instance_mailing.id)
                
            else:
                return render(request, 'mailing/cursos/edit.html', { 
                                                                        'form': form, 
                                                                        'instance_mailing': instance_mailing, 
                                                                        'image_hash': instance_mailing.images_hash,
                                                                        'attachment_hash': instance_mailing.attachment_hash
                                                                    })
        else:
            if request.user.is_staff:
                form = StaffMailingForm(instance=instance_mailing)
            else:
                form = UserMailingForm(instance=instance_mailing)
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
        return redirect('list.curs.mailings', curs_id=curs_id)

@user_passes_test(lambda u: u.is_staff)
def show_mailing_curs(request, curs_id, mailing_id):
    try:
        instance_curs = Curs.objects.filter(id=curs_id)[0]
        
        instance_mailing = Mailing.objects.filter(curs__id=curs_id)[0]
        
        return render(request, 'mailing/classes/show.html', { 
                                                                'instance_mailing': instance_mailing, 
                                                                'instance_curs': instance_curs,
                                                                'image_hash': instance_mailing.images_hash,
                                                                'attachment_hash': instance_mailing.attachment_hash
                                                            })

    except Exception as e:
        if settings.DEBUG:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        return redirect('list.curs.mailings', curs_id=curs_id)

@user_passes_test(lambda u: u.is_staff)
def enviar_mailing_curs(request, curs_id, mailing_id):
    try:      
        instance_mailing = Mailing.objects.filter(id=mailing_id)[0]

        instance_curs = Curs.objects.filter(id=curs_id).first()

        classes = instance_curs.classes.all()

        for classe_instance in classes:
            instance_mailing.classes.add(classe_instance)
        instance_mailing.save()
        
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                instance_mailing.status = MAILING_STATUS_PROGRAMAT
                instance_mailing.save()
                messages.info(request, 'e-Mail programat per enviar-se')

                return redirect('list.curs.mailings', curs_id=curs_id)
            else:
                messages.error(request, 'Programant l\'enviament')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'mailing/cursos/enviar.html', { 'instance_mailing': instance_mailing, 'instance_curs': instance_curs })

    except Exception as e:
        print(str(e))
        return redirect('list.curs.mailings', curs_id=curs_id)