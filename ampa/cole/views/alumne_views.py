from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

from cole.forms import *

import time
import sys
import os

@login_required
def edit_alumne(request, classe_id, alumne_id=None):
    try:
        if request.user.is_staff:
            classe_instance = Classe.objects.filter(id=classe_id).first()
        else:
            classe_instance = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user)).first()

        if alumne_id:
            alumne_instance = Alumne.objects.filter(classes=classe_instance, id=alumne_id).first()
            new_alumne = False
        else:
            alumne_instance = Alumne()
            new_alumne = True

        view_hash = {
                        'alumne_id': alumne_id, 
                        'classe_id': classe_id,
                        'classe_nom': classe_instance.nom,
                        'alumne_instance': alumne_instance,
                        'staff_view': request.user.is_staff,
                        'new_alumne': new_alumne
                    }
        if not alumne_id:
            view_hash['extrainfo_hash'] = alumne_instance.extrainfo_hash

        if request.method == 'POST':
            form = EditAlumneForm(request.POST, staff_view=request.user.is_staff, instance=alumne_instance)
            view_hash['form'] = form
            if form.is_valid():
                form.save()
                classe_instance.alumnes.add(alumne_instance)
                messages.info(request, 'Dades guardades correctament')
                try:
                    afegir_altres_dades = form.data['altres']
                    return redirect('add.extrainfo.alumne', alumne_id=alumne_instance.id)
                except Exception as e:
                    pass
            else:
                return render(request, 'alumnes/edit.html', view_hash)
            return redirect('show.classe', classe_id=classe_id)
        else:
            form = EditAlumneForm(staff_view=request.user.is_staff, instance=alumne_instance)
            view_hash['form'] = form
            print(str(view_hash))
        return render(request, 'alumnes/edit.html', view_hash)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))
        return redirect('list.classes')

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
            extrainfo_instance = ExtraInfoAlumne.objects.filter(id=extrainfo_id, alumne__id=alumne_id).first()
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

@login_required
def edit_alumne_classes(request, alumne_id):
    try:
        alumne_instance = Alumne.objects.filter(id=alumne_id)[0]
        list_classes = alumne_instance.classes.all()

        return render(request, 'alumnes/list_classes.html', {
                                                                'list_classes': list_classes, 
                                                                'alumne_instance': alumne_instance, 
                                                                'user_admin': request.user.is_staff,
                                                            })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('search.edit.alumne', {'alumne_id': alumne_id})

@login_required
def unlink_alumne_classes(request, alumne_id, classe_id):
    try:
        alumne_instance = Alumne.objects.filter(id=alumne_id)[0]
        classe_instance = Classe.objects.filter(id=classe_id)[0]

        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                alumne_instance.classes.remove(classe_instance)
                alumne_instance.save()
                messages.info(request, 'Alumne eliminat de la classe')

                return redirect('show.classe', classe_id=classe_id)
            else:
                messages.error(request, 'Error eliminant la classe')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'alumnes/unlink_classe.html', {'classe_instance': classe_instance, 'alumne_instance': alumne_instance})
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('search.edit.alumne', {'alumne_id': alumne_id})    