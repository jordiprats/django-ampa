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
import os

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /wp-admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def show_classe(request, classe_id):
    if request.user.is_authenticated:
        try:
            instance_classe = Classe.objects.filter(id=classe_id)[0]
            return render(request, 'show_classe.html', {'instance_classe': instance_classe})
        except:
            return redirect('home')
    else:
        return redirect('home')

@login_required
def enviar_nota(request, classe_id=None):
    if classe_id:
        if request.user.is_superuser:
            instance_classe = Classe.objects.filter(id=classe_id)[0]
        else:
            instance_classe = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]
    else:
        return HttpResponse("not implemented", content_type="text/plain")

@login_required
def redirect_to_static(request, topic, file, ext):
    return redirect('http://'+settings.STATIC_URL+'help/'+topic+'/'+file+'.'+ext)

@login_required
def show_help(request, topic=None):
    if topic:
        topic_clean = slugify(topic, allow_unicode=False)

        file_path = os.path.join(settings.STATIC_FULLPATH, 'help', topic_clean+'.md')

        print(file_path)
        try:
            topic_content = Path(file_path).read_text()

            print(topic_content)

            return render(request, 'help.html', {'topic_content': topic_content})
        except Exception as e:
            print(str(e))
            messages.error(request, 'Error accedint al fitxer d\'ajuda')
            return redirect('home')
    else:
        topics = { 'exportXLS': 'Exportar a Excel' }
        return render(request, 'help.html', { 'topics': topics })

@login_required
def edit_classe(request, classe_id=None):
    try:
        if classe_id:
            classe_instance = Classe.objects.filter(id=classe_id)[0]
        else:
            classe_instance = Classe(delegat=request.user)
        if request.method == 'POST':
            form = ClasseForm(request.POST, instance=classe_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'edit_classe.html', { 'form': form, 'classe_id': classe_id, 'classe_instance': classe_instance })
            return redirect('show.classe', classe_id=classe_instance.id)
        else:
            form = ClasseForm(instance=classe_instance)
        return render(request, 'edit_classe.html', { 'form': form, 'classe_id': classe_id, 'classe_instance': classe_instance })
    except Exception as e:
        print(str(e))
        if classe_id:
            return redirect('show.classe', classe_id=classe_id)
        else:
            return redirect('list.classes')

@login_required
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
            return render(request, 'delete_alumne.html', {'instance_alumne': instance_alumne})
        else:
            return redirect('show.classe', classe_id=classe_id)
    except Exception as e:
        print(str(e))
        return redirect('show.classe', classe_id=classe_id)

@login_required
def delete_classe(request, classe_id):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                instance_classe = Classe.objects.filter(id=classe_id)[0]
            else:
                instance_classe = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]
            if request.method == 'POST':
                form = AreYouSureForm(request.POST)
                if form.is_valid():
                    instance_classe.delete()
                    messages.info(request, 'Classe eliminada')

                    return redirect('list.classes')
                else:
                    messages.error(request, 'Error eliminant la classe')
            else:
                form = AreYouSureForm(request.GET)
            return render(request, 'delete_classe.html', {'instance_classe': instance_classe})
        else:
            return redirect('show.classe', classe_id=classe_id)
    except Exception as e:
        print(str(e))
        return redirect('show.classe', classe_id=classe_id)

@login_required
def edit_alumne(request, classe_id, alumne_id=None):
    try:
        classe_instance = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]

        if alumne_id:
            alumne_instance = Alumne.objects.filter(classe=classe_instance, id=alumne_id)[0]
        else:
            alumne_instance = Alumne(classe=classe_instance)
        if request.method == 'POST':
            form = EditAlumneForm(request.POST, instance=alumne_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'edit_alumne.html', { 'form': form, 'alumne_id': alumne_id, 'classe_id': classe_id, 'alumne_instance': alumne_instance})
            return redirect('show.classe', classe_id=classe_id)
        else:
            form = EditAlumneForm(instance=alumne_instance)
        return render(request, 'edit_alumne.html', { 'form': form, 'alumne_id': alumne_id, 'classe_id': classe_id, 'alumne_instance': alumne_instance})
    except Exception as e:
        print(str(e))
        return redirect('list.classes')

def list_classes(request):
    if request.user.is_authenticated:
        if request.user.is_superuser and request.GET.get('admin', ''):
            list_classes = Classe.objects.all()
            return render(request, 'list_classes.html', {'list_classes': list_classes, 'admin': True})
        else:
            list_classes = Classe.objects.filter(Q(delegat=request.user) | Q(subdelegat=request.user))
            return render(request, 'list_classes.html', {'list_classes': list_classes, 'admin': False})
        
    else:
        return redirect('home')

def edit_alumne_form_pares(request, alumne_id):
    try:
        alumne_edit = Alumne.objects.filter(id=alumne_id)[0]

        if request.method == 'POST':
            form = EditAlumneParesForm(request.POST, instance=alumne_edit)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'edit_alumne_form_pares.html', {'form': form, 'instance': alumne_edit, 'message': 'Form invalid'})
            return redirect('home')
        else:
            form = EditAlumneParesForm(instance=alumne_edit)
        return render(request, 'edit_alumne_form_pares.html', {'form': form, 'instance': alumne_edit})
    except Exception as e:
        print(str(e))
        return redirect('home')

def home(request):
    return render(request, 'home.html')

def wait_export(request, classe_id):
    if request.user.is_authenticated:
        try:
            instance_classe = Classe.objects.filter(id=classe_id)[0]
            return render(request, 'wait_classe_export.html', {'instance_classe': instance_classe})
        except Exception as e:
            print(str(e))
            return redirect('show.classe', classe_id=classe_id)
    else:
        return redirect('home')

@login_required
def get_export(request, classe_id, export_name):
    try:
        instance_classe = Classe.objects.filter(id=classe_id, waiting_export=False, latest_export=export_name)[0]

        file_path = os.path.join(settings.XLS_ROOT, 'export/', instance_classe.latest_export)

        test_file = open(file_path, 'rb')
        response = HttpResponse(content=test_file)
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return response
    except Exception as e:
        print(str(e))
        return redirect('show.classe', classe_id=classe_id)

def upload_xls(request):
    if request.user.is_authenticated:
        try:
            if request.method == 'POST' and request.FILES['xlsfile']:
                myfile = request.FILES['xlsfile']
                fs = FileSystemStorage(location=settings.XLS_ROOT+'/'+str(int(time.time())))
                filename = fs.save(myfile.name, myfile)
                try:
                    current_classe = Classe.objects.filter(nom=request.POST['classe'], curs=request.POST['curs'])[0]
                except IndexError:
                    current_classe = Classe(nom=request.POST['classe'], curs=request.POST['curs'], delegat=request.user)
                    current_classe.save()

                upload = FileUpload(filepath=fs.location+'/'+filename, owner=request.user, classe=current_classe)
                upload.save()

                #return render(request, 'upload.html', {'uploaded_file_url': upload.filepath})
                return redirect('show.classe', classe_id=upload.classe.id)
        except Exception as e:
            messages.error(request, 'Error pujant XLS')
            if request.user.is_superuser:
                messages.error(request, str(e))
            return render(request, 'upload.html')

        return render(request, 'upload.html')
    else:
        return redirect('home')

@login_required
def exportar_classe(request, classe_id):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                instance_classe = Classe.objects.filter(id=classe_id)[0]
            else:
                instance_classe = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]

            if request.method == 'POST':
                form = AreYouSureForm(request.POST)
                if form.is_valid():
                    # export classe
                    if instance_classe.latest_export:
                        try:
                            os.remove(os.path.join(settings.XLS_ROOT, 'export', instance_classe.latest_export))
                        except:
                            pass
                        instance_classe.latest_export = None
                    instance_classe.waiting_export = True

                    instance_classe.save()
                    # redirect export
                    return redirect('wait.export', classe_id=instance_classe.id)
                else:
                    messages.error(request, 'Error programant exportació de dades')
            else:
                form = AreYouSureForm(request.GET)
            return render(request, 'do_export.html', {'instance_classe': instance_classe})
        else:
            return redirect('home')
    except Exception as e:
        print(str(e))
        return redirect('home')    

def are_you_sure_email(request, classe_id):
    try:
        if request.user.is_authenticated:
            instance_classe = Classe.objects.filter(id=classe_id, ultim_email=None, ready_to_send=False)[0]

            if request.method == 'POST':
                form = AreYouSureForm(request.POST)
                if form.is_valid():
                    messages.info(request, 'Programat l\'enviament de emails')

                    instance_classe.ready_to_send = True
                    instance_classe.save()

                    return redirect('show.classe', classe_id=instance_classe.id)
                else:
                    messages.error(request, 'Error programent enviament')
            else:
                form = AreYouSureForm(request.GET)
            return render(request, 'email_ready.html', {'instance_classe': instance_classe})
        else:
            return redirect('home')
    except Exception as e:
        print(str(e))
        return redirect('home')

def login_builtin_user(request):
    if request.method == 'POST':
        next = request.POST.get('next', None)
        if next and '://' in next:
            next = None
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {'message': 'User not found or password invalid'})
    else:
        next = request.GET.get('next', None)
        if next and '://' in next:
            next = None
        return render(request, 'login.html', { 'next': next })

def logout_builtin_user(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = WIUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user,backend='cole.backends.EmailBackend')
            return redirect('home')
    else:
        form = WIUserCreationForm()
    return render(request, 'signup.html', {'form': form})
