from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from cole.models import *
from cole.forms import *

import time

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
def add_classe(request):
    try:
        classe_instance = Classe(delegat=request.user, nom='', curs='')
        if request.method == 'POST':
            classe_instance = Classe(delegat=request.user)
            form = ClasseForm(request.POST, instance=classe_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'add_classe.html', { 'form': form })
            return redirect('home')
        else:
            form = ClasseForm(instance=classe_instance)
        return render(request, 'add_classe.html', { 'form': form })
    except Exception as e:
        print(str(e))
        return redirect('home')


@login_required
def edit_alumne(request, classe_id, alumne_id=None):
    try:
        classe_instance = Classe.objects.filter(delegat=request.user, id=classe_id)[0]

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
                return render(request, 'add_alumne.html', { 'form': form, 'alumne_id': alumne_id})
            return redirect('home')
        else:
            form = EditAlumneForm(instance=alumne_instance)
        return render(request, 'add_alumne.html', { 'form': form, 'alumne_id': alumne_id})
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
        except:
            messages.error(request, 'Error pujant XLS')
            return render(request, 'upload.html')

        return render(request, 'upload.html')
    else:
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
                    messages.error(request, 'Error de login')
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
