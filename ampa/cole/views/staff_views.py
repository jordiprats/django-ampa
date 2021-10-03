from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

from cole.models import *
from cole.forms import *

import time
import sys
import os


@user_passes_test(lambda u: u.is_staff)
def upload_entitat_logo(request):
    try:
        entitat_instance = Entitat.objects.first()
        if request.method == 'POST' and request.FILES['logo']:
            myfile = request.FILES['logo']
            upload_subdir = str(int(time.time()))
            fs = FileSystemStorage(location=settings.UPLOADS_ROOT+'/'+upload_subdir)
            filename = fs.save(myfile.name, myfile)

            upload = FileAttachment(filename=myfile.name, filepath=fs.location+'/'+filename, upload_path=upload_subdir)
            upload.save()

            entitat_instance.logo = upload
            entitat_instance.save()

            return redirect('staff.settings')
    except Exception as e:
        print(str(e))
        messages.error(request, 'Error pujant logo')
        if request.user.is_staff:
            messages.error(request, str(e))
        if settings.DEBUG:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))

    return render(request, 'staff/entitat/upload_logo.html')

@user_passes_test(lambda u: u.is_staff)
def edit_entitat(request):
    try:
        try:
            entitat_instance = Entitat.objects.all()[0]
        except:
            entitat_instance = Entitat()

        print(entitat_instance.name)

        if request.method == 'POST':
            print("POST "+str(entitat_instance.name))
            form = EntitatForm(request.POST, instance=entitat_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades')
                return redirect('edit.entitat')
            else:
                messages.error(request, 'Error guardant')
        else:
            form = EntitatForm(instance=entitat_instance)
        return render(request, 'staff/entitat/edit.html', { 'entitat_instance': entitat_instance, 'form': form })

    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        return redirect('edit.entitat')

@user_passes_test(lambda u: u.is_staff)
def edit_curs_modalitat(request, modalitat_id=None):
    try:
        if modalitat_id:
            modalitat_instance = Modalitat.objects.filter(id=modalitat_id).first()
            new = False
        else:
            modalitat_instance = Modalitat()
            new = True

        if request.method == 'POST':
            form = ModalitatForm(request.POST, instance=modalitat_instance)
            if form.is_valid():
                form.save()
                return redirect('staff.settings')
            else:
                messages.error(request, 'Error de validació')
        else:
            form = ModalitatForm(instance=modalitat_instance)
        return render(request, 'cursos/modalitats/edit.html', { 'modalitat_instance': modalitat_instance, 'new': new, 'form': form })

    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        return redirect('show.classe', classe_id=classe_id)

@user_passes_test(lambda u: u.is_staff)
def list_curs_modalitats(request):
    list_modalitats = Modalitat.objects.all()
    return render(request, 'cursos/modalitats/list.html', {
                                                            'list_modalitats': list_modalitats, 
                                                            'public': False, 
                                                            'user_admin': request.user.is_staff
                                                        }) 

@user_passes_test(lambda u: u.is_staff)
def delete_alumne(request, classe_id, alumne_id):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                instance_alumne = Alumne.objects.filter(id=alumne_id, classe__id=classe_id)[0]
            else:
                instance_alumne = Alumne.objects.filter(id=alumne_id, classe__id=classe_id).filter(Q(classe__delegat=request.user) | Q(classe__subdelegat=request.user))[0]
            if request.method == 'POST':
                form = AreYouSureForm(request.POST)
                if form.is_valid():
                    instance_alumne.delete()
                    messages.info(request, 'Alumne eliminat')

                    return redirect('show.classe', classe_id=classe_id)
                else:
                    messages.error(request, 'Error eliminant l\'alumne')
            else:
                form = AreYouSureForm(request.GET)
            return render(request, 'alumnes/delete.html', {'instance_alumne': instance_alumne})
        else:
            return redirect('show.classe', classe_id=classe_id)
    except Exception as e:
        print(str(e))
        return redirect('show.classe', classe_id=classe_id)

@user_passes_test(lambda u: u.is_staff)
def add_alumne_classe(request, classe_id, alumne_id):
    try:
        classe_instance = Classe.objects.filter(id=classe_id).first()
        alumne_instance = Alumne.objects.filter(id=alumne_id).first()

        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                alumne_instance.classes.add(classe_instance)
                alumne_instance.save()
                return redirect('show.classe', classe_id=classe_id)
            else:
                messages.error(request, 'Error de validació')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'alumnes/add_to_classe.html', { 'classe_instance': classe_instance, 'alumne_instance': alumne_instance, 'form': form })


    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        return redirect('show.classe', classe_id=classe_id)

@user_passes_test(lambda u: u.is_staff)
def search_alumne_by_phone(request):
    try:
        phone = request.GET.get('q', '')
        if phone:
            llistat_alumnes = Alumne.objects.filter(Q(telf_tutor1__icontains=phone) | Q(telf_tutor1__icontains=phone) )
        else:
            llistat_alumnes = Alumne.objects.none()
        return render(request, 'alumnes/add.classe.search.html', { 
                                                                    'llistat_alumnes': llistat_alumnes, 
                                                                    'classe_id': None, 
                                                                    'classe_full_nom': None
                                                                })
    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        return redirect('alumne.search.by.phone', classe_id=classe_id)

@user_passes_test(lambda u: u.is_staff)
def add_classe_search_alumne(request, classe_id=None):
    try:
        if classe_id:
            classe_instance = Classe.objects.filter(id=classe_id).first()
            classe_full_nom =  classe_instance.full_nom
        else:
            classe_full_nom = None
        
        query = request.GET.get('q', '')
        if query:
            llistat_alumnes = Alumne.objects.filter(Q(nom_unaccented__icontains=query) | Q(cognom1_unaccented__icontains=query) | Q(cognom2_unaccented__icontains=query))
        else:
            llistat_alumnes = None
        return render(request, 'alumnes/add.classe.search.html', { 
                                                                    'llistat_alumnes': llistat_alumnes, 
                                                                    'classe_id': classe_id, 
                                                                    'classe_full_nom': classe_full_nom
                                                                })
    except Exception as e:
        if request.user.is_staff:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            messages.error(request, str(e))
        return redirect('show.classe', classe_id=classe_id)

@user_passes_test(lambda u: u.is_staff)
def staff_settings(request):
    etapes = Etapa.objects.all()
    cursos = Curs.objects.all()[:3]

    return render(request, 'staff/settings.html', { 'user': request.user, 'etapes': etapes, 'cursos': cursos })


@user_passes_test(lambda u: u.is_staff)
def reimport(request, classe_id):
    try:
        if request.method == 'POST':
            instance_classe = Classe.objects.filter(id=classe_id).first()
            fileupload = FileUpload.objects.filter(processed=True, error=True, classe=instance_classe).order_by('-updated_at').first()

            fileupload.error=False
            fileupload.processed=False
            fileupload.save()
    except:
        pass    
    return redirect('show.classe', classe_id=classe_id)