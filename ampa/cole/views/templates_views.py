from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages

from cole.forms import *

import time
import sys
import os

@user_passes_test(lambda u: u.is_staff)
def upload_template(request):
    try:
        if request.method == 'POST' and request.FILES['attachment']:
            myfile = request.FILES['attachment']
            upload_subdir = str(int(time.time()))
            fs = FileSystemStorage(location=settings.UPLOADS_ROOT+'/'+upload_subdir)
            filename = fs.save(myfile.name, myfile)

            upload_template = WordTemplate(filename=myfile.name, filepath=fs.location+'/'+filename, upload_path=upload_subdir)
            upload_template.save()

            messages.info(request, 'Fitxer pujat correctament')
            if request.user.is_superuser:
                messages.info(request, upload_template.filepath)
                messages.info(request, upload_template.static_url)
            return redirect('peticions.list.templates')
        else:
            return render(request, 'templates/upload.html', {})
    except Exception as e:
        messages.error(request, 'Error pujant arxiu')
        if request.user.is_superuser:
            messages.error(request, str(e))
    return redirect('peticions.list.templates')

@user_passes_test(lambda u: u.is_staff)
def list_templates(request):
    list_templates = WordTemplate.objects.all()
    return render(request, 'templates/list.html', {
                                                    'list_templates': list_templates, 
                                                })