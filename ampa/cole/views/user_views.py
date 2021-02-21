from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

from cole.forms import *

import sys
import os

@user_passes_test(lambda u: u.is_staff)
def users_list(request):
    pass

@login_required
def user_settings(request):
    if request.method == 'POST':
        form = AMPAUserName(request.POST)
        if form.is_valid():
            request.user.name = form.data['name'][0]
            request.user.save()
            return redirect('user.settings')
        else:
            messages.error(request, 'Error guardant dades')
    else:
        form = AMPAUserName(request.GET, initial={'name': request.user.name})
    return render(request, 'users/settings.html', { 'user': request.user, 'form': form })    

@login_required
def change_password(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = PasswordChangeForm(request.POST)
                if form.is_valid():
                    try:
                        if request.user.check_password(form.data['password_actual'][0]):
                            request.user.set_password(form.data['password1'][0])
                            request.user.save()
                            update_session_auth_hash(request, request.user)
                            messages.info(request, 'Contrasenya actualitzada')
                            return redirect('home')
                        else:
                            messages.error(request, 'Contrasenya actual incorrecte')
                    except Exception as e:
                        #if request.user.is_superuser:
                        messages.error(request, 'Error canviant la contrasenya: '+str(e))
                else:
                    messages.error(request, 'Error al canviar la contrasenya')
            else:
                form = PasswordChangeForm(request.GET)
            return render(request, 'users/password_change.html', { 'form': form } )
 
    except Exception as e:
        if settings.DEBUG:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
    return redirect('home')