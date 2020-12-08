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

        return render(request, 'cursos/show.html', { 'curs_instance': curs_instance, 'list_classes': curs_instance.classes.all() })
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