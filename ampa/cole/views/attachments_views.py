from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.utils.text import slugify
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from pathlib import Path

from cole.models import *
from cole.forms import *

import time
import sys
import os


@login_required
def remove_attachment_mailing(request, mailing_id, attachment_id):
    try:
        instance_mailing = Mailing.objects.filter(id=mailing_id)[0]

        if instance_mailing.etapa or instance_mailing.curs:
            if not request.user.is_staff:
                raise Exception('Not staff')

        instance_attachment = FileAttachment.objects.filter(id=attachment_id)[0]
        
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                instance_mailing.attachments.remove(instance_attachment)
                instance_mailing.save()
                if instance_attachment.mailings.count() == 0:
                    instance_attachment.delete()
                messages.info(request, 'Fitxer adjunt eliminat')

                if instance_mailing.classes.count() == 1:
                    return redirect('list.classe.mailings', classe_id=instance_mailing.classes.all()[0].id)
                else:
                    # TODO
                    return redirect('home')
            else:
                messages.error(request, 'Error eliminant l\'alumne')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'mailing/attachments/delete.html', { 'instance_mailing': instance_mailing, 'instance_attachment': instance_attachment })

    except Exception as e:
        if settings.DEBUG:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        if instance_mailing.classes.count() == 1:
            return redirect('list.classe.mailings', classe_id=instance_mailing.classes.all()[0].id)
        elif instance_mailing.curs:
            return redirect('edit.curs.mailing', curs_id=instance_mailing.curs.id, mailing_id=instance_mailing.id)
        else:
            # TODO
            return redirect('home')


@login_required
def afegir_attachment_mailing_classe(request, mailing_id):
    try:
        instance_mailing = Mailing.objects.filter(id=mailing_id)[0]

        if instance_mailing.etapa or instance_mailing.curs:
            if not request.user.is_staff:
                raise Exception('Not staff')

        if request.method == 'POST' and request.FILES['attachment']:
            myfile = request.FILES['attachment']
            upload_subdir = str(int(time.time()))
            fs = FileSystemStorage(location=settings.UPLOADS_ROOT+'/'+upload_subdir)
            filename = fs.save(myfile.name, myfile)

            upload = FileAttachment(filename=myfile.name, filepath=fs.location+'/'+filename, upload_path=upload_subdir)
            upload.save()

            instance_mailing.attachments.add(upload)
            instance_mailing.save()

            messages.info(request, 'Fitxer pujat correctament')
            if request.user.is_superuser:
                messages.info(request, upload.filepath)
                messages.info(request, upload.static_url)
            if instance_mailing.classes.count() == 1:
                return redirect('edit.classe.mailing', classe_id=instance_mailing.classes.all()[0].id, mailing_id=instance_mailing.id)
                # return redirect('list.classe.mailings', classe_id=instance_mailing.classes.all()[0].id)
            elif instance_mailing.curs:
                return redirect('edit.curs.mailing', curs_id=instance_mailing.curs.id, mailing_id=instance_mailing.id)
            else:
                # TODO
                return redirect('home')
        else:
            return render(request, 'mailing/attachments/upload.html', { 'instance_mailing': instance_mailing })
    except Exception as e:
        messages.error(request, 'Error pujant arxiu')
        if request.user.is_superuser:
            messages.error(request, str(e))
    return redirect('home')