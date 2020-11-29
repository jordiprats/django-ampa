from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from cole.forms import *

import time
import sys
import os

@login_required
def search_edit_alumne(request, alumne_id):
    try:
        alumne_instancia = Alumne.objects.filter(id=alumne_id).first()
        return redirect('edit.alumne', classe_id=alumne_instancia.classe.id, alumne_id=alumne_id)
    except:
        return redirect('home')

@user_passes_test(lambda u: u.is_staff)
def edit_extrainfo_alumne(request, alumne_id, extrainfo_id=None):
    try:
        alumne_instance = Alumne.objects.filter(id=alumne_id).first()

        if extrainfo_id:
            extrainfo_instance = ExtraInfoAlumne.objects.filter(id=extrainfo_id, alumne__id=alumne_id)[0]
        else:
            extrainfo_instance = ExtraInfoAlumne(alumne=alumne_instance)
        if request.method == 'POST':
            form = InfoAlumneForm(request.POST, instance=extrainfo_instance)
            if form.is_valid():
                try:
                    if request.FILES['attachment']:
                        myfile = request.FILES['attachment']
                        upload_subdir = str(int(time.time()))
                        fs = FileSystemStorage(location=settings.UPLOADS_ROOT+'/'+upload_subdir)
                        filename = fs.save(myfile.name, myfile)

                        upload = FileAttachment(filename=myfile.name, filepath=fs.location+'/'+filename, upload_path=upload_subdir)
                        upload.save()

                        extrainfo_instance.attachment=upload
                except Exception as e:
                    if request.user.is_staff:
                        messages.error(request, str(e))
                    pass
                extrainfo_instance.save()
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'alumnes/extra/upload.html', { 
                                                                        'form': form, 
                                                                        'extrainfo_instance': extrainfo_instance,
                                                                        'fileattachment': extrainfo_instance.attachment,
                                                                        'alumne_instance': alumne_instance
                                                                    })
            return redirect('search.edit.alumne', alumne_id=alumne_id)
        else:
            form = InfoAlumneForm(instance=extrainfo_instance)
        return render(request, 'alumnes/extra/upload.html', { 
                                                                'form': form, 
                                                                'extrainfo_instance': extrainfo_instance,
                                                                'fileattachment': extrainfo_instance.attachment,
                                                                'alumne_instance': alumne_instance
                                                            })
    except Exception as e:
        if request.user.is_staff:
            messages.error(request, str(e))
        return redirect('search.edit.alumne', alumne_id=alumne_id)