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

        return render(request, 'etapes/show.html', { 'etapa_instance': etapa_instance, 'list_classes': etapa_instance.classes.all })
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