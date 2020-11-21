from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from cole.forms import User
from cole.forms import AreYouSureForm
from voting.forms import *

def home(request):
    return render(request, 'voting/home.html')

@login_required
def list_elections(request):
    if request.user.is_superuser and request.GET.get('admin', ''):
        list_elections = Election.objects.all()
        return render(request, 'voting/elections/list.html', {'list_elections': list_elections, 'admin_view': True, 'user_admin': request.user.is_staff })
    else:
        list_elections = Election.objects.filter(owner=request.user)
        return render(request, 'voting/elections/list.html', {'list_elections': list_elections, 'admin_view': False, 'user_admin': request.user.is_staff })


@login_required
def edit_election(request, election_id=None):
    try:
        if election_id:
            if request.user.is_staff:
                election_instance = Election.objects.filter(id=election_id)[0]
            else:
                election_instance = Election.objects.filter(id=election_id, owner=request.user)[0]
        else:
            election_instance = Election(owner=request.user)
        if request.method == 'POST':
            form = ElectionForm(request.POST, instance=election_instance)
            if form.is_valid():
                form.save()
                
                try:
                    boto_apretat = str(form.data['guardar'])
                    messages.info(request, 'Dades guardades correctament')
                    return redirect('voting.list.elections')
                except:
                    try:
                        boto_apretat = str(form.data['alguna_pregunta_mes'])
                        return redirect('voting.add.option', election_id=election_instance.id)
                    except:
                        for element in form.data:
                            if element.startswith('editar_opcio_'):
                                return redirect('voting.edit.option', election_id=election_instance.id, option_id=element.split('_')[2])
                        return redirect('voting.add.option', election_id=election_instance.id)
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'voting/elections/edit.html', { 'form': form, 'election_id': election_id, 'election_instance': election_instance })
        else:
            form = ElectionForm(instance=election_instance)
        return render(request, 'voting/elections/edit.html', { 'form': form, 'election_id': election_id, 'election_instance': election_instance })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(str(e))
        if election_id:
            return redirect('voting.edit.election', election_id=election_instance.id)
        else:
            return redirect('voting.list.elections')

def show_election(request, election_id):
    pass

@login_required
def edit_option(request, election_id, option_id=None):
    try:
        if request.user.is_staff:
            election_instance = Election.objects.filter(id=election_id)[0]
        else:
            election_instance = Election.objects.filter(id=election_id, owner=request.user)[0]

        if option_id:
            option_instance = Option.objects.filter(election=election_instance, id=option_id)[0]
        else:
            option_instance = Option(election=election_instance)


        if request.method == 'POST':
            form = OptionForm(request.POST, instance=option_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Opció guardada correctament')

                return redirect('voting.edit.election', election_id=election_id)
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'voting/options/edit.html', { 
                                                                        'form': form, 
                                                                        'election_instance': election_instance, 
                                                                        'option_instance': option_instance
                                                                    })
        else:
            form = OptionForm(instance=option_instance)
            return render(request, 'voting/options/edit.html', { 
                                                                    'form': form, 
                                                                    'election_instance': election_instance, 
                                                                    'option_instance': option_instance
                                                                })

    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('voting.edit.election', election_id=election_id)

@login_required
def delete_option(request, election_id, option_id):
    try:
        if request.user.is_staff:
            election_instance = Election.objects.filter(id=election_id)[0]
        else:
            election_instance = Election.objects.filter(id=election_id, owner=request.user)[0]

        if option_id:
            option_instance = Option.objects.filter(election=election_instance, id=option_id)[0]
        else:
            option_instance = Option(election=election_instance)
        
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                option_instance.delete()
                messages.info(request, 'Opció eliminada')
                return redirect('voting.edit.election', election_id=election_id)
            else:
                messages.error(request, 'Error eliminant l\'alumne')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'voting/options/delete.html', { 'option_instance': option_instance })

    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('voting.edit.election', election_id=election_id)