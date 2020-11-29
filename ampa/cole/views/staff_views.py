from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from cole.forms import *

import sys
import os

@user_passes_test(lambda u: u.is_staff)
def staff_settings(request):
    return render(request, 'staff/settings.html', { 'user': request.user })    

@user_passes_test(lambda u: u.is_staff)
def list_cursos(request):
    cursos = Curs.objects.all()

    return render(request, 'cursos/list.html', {'cursos': cursos })

@user_passes_test(lambda u: u.is_staff)
def show_curs(request, curs_id):
    try:
        curs_instance = Curs.objects.filter(id=curs_id)[0]

        return render(request, 'cursos/show.html', { 'curs_instance': curs_instance })
    except Exception as e:
        if request.user.is_staff:
            if settings.debug:
                print(str(e))
            messages.error(request, str(e))
        return redirect('staff.settings')

@user_passes_test(lambda u: u.is_staff)
def edit_curs(request, curs_id=None):
    try:
        if curs_id:
            curs_instance = Curs.objects.filter(id=curs_id)[0]
        else:
            curs_instance = Curs()
        if request.method == 'POST':
            form = CursForm(request.POST, instance=curs_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'cursos/edit.html', { 'form': form, 'curs_instance': curs_instance })
            return redirect('show.curs', curs_id=curs_instance.id)
        else:
            form = CursForm(instance=curs_instance)
        return render(request, 'cursos/edit.html', { 'form': form, 'curs_instance': curs_instance })
    except Exception as e:
        if request.user.is_staff:
            if settings.debug:
                print(str(e))
            messages.error(request, str(e))
        if curs_id:
            return redirect('show.curs', curs_id=curs_id)
        else:
            return redirect('staff.settings')