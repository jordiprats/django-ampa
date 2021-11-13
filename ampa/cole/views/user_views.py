from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from cole.forms import *

import datetime
import sys
import os

@user_passes_test(lambda u: u.is_staff)
def switch_user(request, user_slug):
    try:
        user_instance = User.objects.filter(slug=user_slug)[0]

        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                login(request, user_instance)
                messages.info(request, 'Canvi d\'usuari completat')
                return redirect('home')
            else:
                messages.error(request, 'Error fent el canvi d\'usuari')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'staff/users/su.html', {'user_instance': user_instance})
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('list.users')

@user_passes_test(lambda u: u.is_staff)
def reset_proteccio_dades(request):
    if request.method == 'POST':
        form = AreYouSureForm(request.POST)
        curs = Curs.objects.first()
        if form.is_valid():
            classes = Classe.objects.filter(curs=curs)
            for classe in classes:
                for alumne in classe.alumnes.all():
                    try:
                        alumne.tutor1_cessio = False
                        alumne.tutor2_cessio = False
                        alumne.save()
                    except:
                        pass
            messages.info(request, 'Eliminada configuració d\'enviaments')
        else:
            messages.error(request, 'Error resetejant')
        return redirect('list.users')
    else:
        form = AreYouSureForm()
        list_users = User.objects.filter(is_staff=False, is_default_password=False)
        return render(request, 'staff/users/reset_proteccio_dades.html', {'form': form, 'list_users': list_users})

@user_passes_test(lambda u: u.is_staff)
def reset_password_all_users(request):
    if request.method == 'POST':
        form = AreYouSureForm(request.POST)
        entitat = Entitat.objects.all().first()
        if form.is_valid():
            for user in User.objects.filter(is_staff=False, is_default_password=False):
                try:
                    user.set_password(entitat.password_default)
                    user.is_default_password = True
                    user.last_password_change = datetime.datetime.now()
                    user.save()
                except:
                    pass
            messages.info(request, 'Contrasenyes resetejades')
        else:
            messages.error(request, 'Error resetejant les contrasenyes')
        return redirect('list.users')
    else:
        form = AreYouSureForm()
        list_users = User.objects.filter(is_staff=False, is_default_password=False)
        return render(request, 'staff/users/reset_password_all_users.html', {'form': form, 'list_users': list_users})

@user_passes_test(lambda u: u.is_staff)
def edit_user(request, user_slug):
    try:
        user_instance = User.objects.filter(slug=user_slug)[0]

        if request.method == 'POST':
            form = AdminEditUser(request.POST, instance=user_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Guardada configuració de l\'usuari')
                return redirect('list.users')
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'staff/users/edit.html', { 
                                                        'form': form, 
                                                        'user_instance': user_instance, 
                                                    })
        else:
            form = AdminEditUser(instance=user_instance)
            return render(request, 'staff/users/edit.html', { 
                                                                    'form': form, 
                                                                    'user_instance': user_instance, 
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('list.users')   

@user_passes_test(lambda u: u.is_staff)
def users_list(request):
    list_users = User.objects.all()

    for user in list_users:
        if user.is_default_password:
            max_allowed = timezone.now() - datetime.timedelta(days=7)
            if user.last_password_change and user.last_password_change < max_allowed:
                user.is_locked = True
                user.save()
        else:
            if not user.is_staff:
                max_allowed = timezone.now() - datetime.timedelta(days=400)
                if user.last_password_change and user.last_password_change < max_allowed:
                    user.is_locked = True
                    user.save()
    return render(request, 'staff/users/list.html', {
                                                      'list_users': list_users, 
                                                    })

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
def change_password(request, user_slug=None):
    try:
        if request.user.is_authenticated:
            if user_slug and request.user.is_staff:
                user_instance = User.objects.filter(slug=user_slug).first()
            else:
                user_instance = request.user
            if request.method == 'POST':
                if request.user.is_staff:
                    form = StaffPasswordChangeForm(request.POST)
                else:
                    form = PasswordChangeForm(request.POST)
                if form.is_valid():
                    try:
                        try:
                            password_actual = form.data['password_actual'][0]
                        except:
                            password_actual = ""
                        
                        is_default = False
                        if request.user.is_staff:
                            try:
                                is_default = form.data['is_default'][0] == "on"
                            except:
                                is_default = False                        

                        if user_instance.check_password(password_actual) or request.user.is_staff:
                            user_instance.set_password(form.data['password1'][0])
                            user_instance.last_password_change = datetime.datetime.now()
                            user_instance.is_default_password = is_default
                            if request.user.is_staff:
                                user_instance.is_locked = False
                            user_instance.save()
                            if not request.user.is_staff:
                                update_session_auth_hash(request, user_instance)
                            messages.info(request, 'Contrasenya actualitzada')
                            if request.user.is_staff:
                                return redirect('list.users')
                            else:
                                return redirect('home')
                        else:
                            messages.error(request, 'Contrasenya actual incorrecte')
                    except Exception as e:
                        #if request.user.is_superuser:
                        messages.error(request, 'Error canviant la contrasenya: '+str(e))
                else:
                    messages.error(request, 'Error al canviar la contrasenya')
            else:
                if request.user.is_staff:
                    form = StaffPasswordChangeForm(request.GET)
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