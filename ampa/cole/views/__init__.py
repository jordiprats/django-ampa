from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.utils.text import slugify
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from pathlib import Path

from cole.views.attachments_views import *
from cole.views.templates_views import *
from cole.views.alumne_views import *
from cole.views.cursos_views import *
from cole.views.etapes_views import *
from cole.views.staff_views import *
from cole.views.user_views import *
from cole.models import *
from cole.forms import *

import time
import sys
import os

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

@login_required
def show_classe(request, classe_id):
    if request.user.is_authenticated:
        try:
            instance_classe = Classe.objects.filter(id=classe_id)[0]
            return render(request, 'classes/show.html', { 
                                                            'instance_classe': instance_classe, 
                                                            'content': 'overview', 
                                                            'is_staff': request.user.is_staff
                                                        })
        except Exception as e:
            print(str(e))
            return redirect('home')
    else:
        return redirect('home')
            
@login_required
def list_classe_mailings(request, classe_id):
    if request.user.is_staff:
        instance_classe = Classe.objects.filter(id=classe_id)[0]
    else:
        instance_classe = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]
    
    list_mailings = Mailing.objects.filter(classes__id=instance_classe.id)

    return render(request, 'classes/show.html', { 'instance_classe': instance_classe, 'list_mailings': list_mailings, 'content': 'mailing' })

@login_required
def enviar_mailing_classe(request, classe_id, mailing_id):
    try:
        if request.user.is_staff:
            instance_classe = Classe.objects.filter(id=classe_id)[0]
        else:
            instance_classe = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]
        
        instance_mailing = Mailing.objects.filter(classes__id=instance_classe.id)[0]
        
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                instance_mailing.status = MAILING_STATUS_PROGRAMAT
                instance_mailing.save()
                messages.info(request, 'e-Mail programat per enviar-se')

                return redirect('list.classe.mailings', classe_id=instance_classe.id)
            else:
                messages.error(request, 'Error eliminant l\'alumne')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'mailing/classes/enviar.html', { 'instance_mailing': instance_mailing, 'instance_classe': instance_classe })

    except Exception as e:
        print(str(e))
        return redirect('show.classe', classe_id=classe_id)

@login_required
def show_mailing_classe(request, classe_id, mailing_id):
    try:
        if request.user.is_staff:
            instance_classe = Classe.objects.filter(id=classe_id)[0]
        else:
            instance_classe = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]
        
        instance_mailing = Mailing.objects.filter(classes__id=instance_classe.id)[0]
        
        return render(request, 'mailing/classes/show.html', { 
                                                                'instance_mailing': instance_mailing, 
                                                                'instance_classe': instance_classe,
                                                                'image_hash': instance_mailing.images_hash,
                                                                'attachment_hash': instance_mailing.attachment_hash
                                                            })

    except Exception as e:
        if settings.DEBUG:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        return redirect('show.classe', classe_id=classe_id)

@login_required
def editar_mailing_classe(request, classe_id, mailing_id=None):
    try:
        if request.user.is_staff:
            instance_classe = Classe.objects.filter(id=classe_id)[0]
        else:
            instance_classe = Classe.objects.filter(id=classe_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user))[0]
        
        if mailing_id:
            instance_mailing = Mailing.objects.filter(classes__id=instance_classe.id, id=mailing_id)[0]
        else:
            instance_mailing = Mailing(email_from='', email_reply_to=request.user.email)
        
        if request.method == 'POST':
            form = ClasseMailingForm(request.POST, instance=instance_mailing)
            if form.is_valid():
                form.save()
                instance_mailing.classes.add(instance_classe)
                instance_mailing.save()
                messages.info(request, 'Guardat mailing')

                try:
                    boto_apretat = str(form.data['guardar'])
                    return redirect('list.classe.mailings', classe_id=instance_classe.id)
                except:
                    return redirect('add.attachment.mailing', mailing_id=instance_mailing.id)
                
            else:
                return render(request, 'mailing/classes/edit.html', { 
                                                                        'form': form, 
                                                                        'instance_mailing': instance_mailing, 
                                                                        'image_hash': instance_mailing.images_hash,
                                                                        'attachment_hash': instance_mailing.attachment_hash
                                                                    })
            return redirect('list.classe.mailings', classe_id=instance_classe.id)
        else:
            form = ClasseMailingForm(instance=instance_mailing)
        return render(request, 'mailing/classes/edit.html', { 
                                                                'form': form, 
                                                                'instance_mailing': instance_mailing, 
                                                                'image_hash': instance_mailing.images_hash,
                                                                'attachment_hash': instance_mailing.attachment_hash
                                                            })

    except Exception as e:
        if settings.DEBUG:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        return redirect('show.classe', classe_id=classe_id)

@login_required
def help_media_redirect_to_static(request, topic, file, ext):
    return redirect(settings.STATIC_DOMAIN+'help/'+topic+'/'+file+'.'+ext)

@login_required
def redirect_to_static(request, file):
    return redirect(settings.STATIC_DOMAIN+file)

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
            curs_instance = Curs.objects.filter(modalitat=None)[0]
            classe_instance = Classe(delegat=request.user, curs=curs_instance)
        if request.method == 'POST':
            if request.user.is_staff:
                form = StaffClasseForm(request.POST, instance=classe_instance)
            else:
                form = ClasseForm(request.POST, instance=classe_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Dades guardades correctament')
            else:
                return render(request, 'classes/edit.html', { 'form': form, 'classe_id': classe_id, 'classe_instance': classe_instance, 'action': 'editar' })
            return redirect('show.classe', classe_id=classe_instance.id)
        else:
            if request.user.is_staff:
                form = StaffClasseForm(instance=classe_instance)
            else:
                form = ClasseForm(instance=classe_instance)
        return render(request, 'classes/edit.html', { 'form': form, 'classe_id': classe_id, 'classe_instance': classe_instance, 'action': 'editar' })
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))
        if classe_id:
            return redirect('show.classe', classe_id=classe_id)
        else:
            return redirect('list.classes')

@login_required
def delete_classe(request, classe_id):
    try:
        if request.user.is_authenticated:
            if request.user.is_staff:
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
            return render(request, 'classes/delete.html', {'instance_classe': instance_classe})
        else:
            return redirect('show.classe', classe_id=classe_id)
    except Exception as e:
        print(str(e))
        return redirect('show.classe', classe_id=classe_id)

@login_required
def list_classes(request, curs_id=None):
    if request.user.is_authenticated:

        if not curs_id:
            curs_instance = Curs.objects.filter(modalitat=None).first()
            curs_id = curs_instance.id

        if request.GET.get('admin', 'NOTSET') == 'NOTSET' and request.user.is_staff:
            url = reverse('list.classes')
            return HttpResponseRedirect(url+'?admin=1')
        # TODO: refactor
        if request.user.is_staff and request.GET.get('admin', '')=='1':
            if curs_id:
                list_classes = Classe.objects.filter(curs__id=curs_id).order_by('curs', 'etapa', 'nom')
            else:
                list_classes = Classe.objects.all().order_by('curs', 'etapa', 'nom')
            return render(request, 'classes/list.html', { 'list_classes': list_classes, 'admin_view': True, 'user_admin': request.user.is_staff })
        else:
            if curs_id:
                list_classes = Classe.objects.filter(curs__id=curs_id).filter(Q(delegat=request.user) | Q(subdelegat=request.user)).order_by('curs', 'etapa', 'nom')
            else:
                list_classes = Classe.objects.filter(Q(delegat=request.user) | Q(subdelegat=request.user)).order_by('curs', 'etapa', 'nom')
            return render(request, 'classes/list.html', { 'list_classes': list_classes, 'admin_view': False, 'user_admin': request.user.is_staff })
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

@login_required
def upload_xls(request, classe_id):
    if request.user.is_authenticated:
        try:
            current_classe = Classe.objects.filter(id=classe_id)[0]
            if request.method == 'POST' and request.FILES['xlsfile']:
                myfile = request.FILES['xlsfile']
                fs = FileSystemStorage(location=settings.XLS_ROOT+'/'+str(int(time.time())))
                filename = fs.save(myfile.name, myfile)

                upload = FileUpload(filepath=fs.location+'/'+filename, owner=request.user)
                upload.classe = current_classe
                upload.save()

                print(upload.classe.nom)

                return redirect('show.classe', classe_id=classe_id)
        except Exception as e:
            print(str(e))
            messages.error(request, 'Error pujant XLS')
            if request.user.is_staff:
                messages.error(request, str(e))
            if settings.DEBUG:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(str(e))

        return render(request, 'classes/upload.html', {'instance_classe': current_classe})
    else:
        return redirect('home')

@user_passes_test(lambda u: u.is_staff)
def copiar_classe(request, classe_id):
    try:
        if classe_id:
            classe_instance = Classe.objects.filter(id=classe_id)[0]
        if request.method == 'POST':
            form = StaffClasseForm(request.POST, instance=classe_instance)
            if form.is_valid():
                new_classe = Classe(delegat=request.user)
                dades_new_classe = form.save(commit=False)

                new_classe.nom = dades_new_classe.nom
                new_classe.alias = dades_new_classe.alias
                new_classe.tutor = dades_new_classe.tutor

                new_classe.curs = dades_new_classe.curs
                new_classe.etapa = dades_new_classe.etapa

                new_classe.nom_delegat = dades_new_classe.nom_delegat
                new_classe.telefon_delegat = dades_new_classe.telefon_delegat
                new_classe.email_delegat = dades_new_classe.email_delegat

                new_classe.nom_subdelegat = dades_new_classe.nom_subdelegat
                new_classe.telefon_subdelegat = dades_new_classe.telefon_subdelegat
                new_classe.email_subdelegat = dades_new_classe.email_subdelegat

                new_classe.delegat = dades_new_classe.delegat
                new_classe.subdelegat = dades_new_classe.subdelegat
                
                new_classe.save()

                for alumne in classe_instance.alumnes.all():
                    alumne.classes.add(new_classe)
                    alumne.save()

                messages.info(request, 'Classe copiada correctament')

                return redirect('show.classe', classe_id=new_classe.id)
            else:
                return render(request, 'classes/edit.html', { 'form': form, 'classe_id': classe_id, 'classe_instance': classe_instance, 'action': 'copiar', 'classe_nom_was': classe_instance.nom })    
        else:
            classe_nom_was = classe_instance.nom
            classe_instance.nom = ""
            classe_instance.alias = ""
            classe_instance.tutor = ""

            classe_instance.nom_delegat = ""
            classe_instance.telefon_delegat = ""
            classe_instance.email_delegat = ""

            classe_instance.nom_subdelegat = ""
            classe_instance.telefon_subdelegat = ""
            classe_instance.email_subdelegat = ""

            form = StaffClasseForm(instance=classe_instance)
        return render(request, 'classes/edit.html', { 'form': form, 'classe_id': classe_id, 'classe_instance': classe_instance, 'action': 'copiar', 'classe_nom_was': classe_nom_was })
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))
        if classe_id:
            return redirect('show.classe', classe_id=classe_id)
        else:
            return redirect('list.classes')

@login_required
def exportar_classe(request, classe_id):
    try:
        if request.user.is_authenticated:
            if request.user.is_staff:
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

def are_you_sure_cessio_dades_email(request, classe_id):
    try:
        if request.user.is_authenticated:
            if request.user.is_staff:
                instance_classe = Classe.objects.filter(id=classe_id)[0]
            else:
                instance_classe = Classe.objects.filter(id=classe_id, ultim_email=None, ready_to_send=False)[0]

            if request.method == 'POST':
                form = AreYouSureForm(request.POST)
                if form.is_valid():
                    messages.info(request, 'Programat l\'enviament de emails')

                    if request.user.is_staff:
                        instance_classe.ultim_email = None

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
        user = authenticate(username=request.POST['login'].lower().strip(), password=request.POST['password'])
        if user is not None:
            if user.is_default_password:
                max_allowed = timezone.now() - datetime.timedelta(days=7)
                if user.last_password_change < max_allowed:
                    messages.error(request, 'El compte està bloquejat. Si us plau, contacti amb l\'administrador.')
                    return redirect('home')
            else:
                if not user.is_staff:
                    max_allowed = timezone.now() - datetime.timedelta(days=400)
                    if user.last_password_change < max_allowed:
                        messages.error(request, 'El compte està bloquejat. Si us plau, contacti amb l\'administrador.')
                        return redirect('home')

            login(request, user)
            # update last login
            user.save()
            if next:
                return redirect(next)
            else:
                if user.is_default_password:
                    return redirect('user.password.change')
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
            username = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            if request.user.is_authenticated:
                if request.user.is_staff:
                    return redirect('home')
            user = authenticate(username=username, password=raw_password)
            login(request, user, backend='cole.backends.EmailBackend')
            return redirect('home')
    else:
        form = WIUserCreationForm()
    return render(request, 'signup.html', {'form': form})
