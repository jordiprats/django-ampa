from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django_xhtml2pdf.utils import generate_pdf
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from docxtpl import DocxTemplate

from peticions.models import *
from peticions.forms import *

from cole.forms import *

import io

#
# staff
#

@user_passes_test(lambda u: u.is_staff)
def preview_docx(request, junta_id):
    try:
        junta_instance = Junta.objects.filter(id=junta_id)[0]
        junta_instance.render_text_version()

        tpl = DocxTemplate("/home/jprats/git/django-ampa/test.docx")

        context = {
                    'junta_instance': junta_instance, 
                    'issue_add_comments': False,
                    'issue_title_size': 'h4',
                    'user_admin': True,
                    'is_pdf': True
                }

        tpl.render(context)
        # tpl.save('./test_output.docx')

        tpl_io = io.BytesIO()
        tpl.save(tpl_io)
        tpl_io.seek(0)

        response = HttpResponse(tpl_io.read())

        # Content-Disposition header makes a file downloadable
        response["Content-Disposition"] = "attachment; filename=preview.docx"

        # Set the appropriate Content-Type for docx file
        response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        return response
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')


@user_passes_test(lambda u: u.is_staff)
def preview_pdf(request, junta_id):
    try:
        junta_instance = Junta.objects.filter(id=junta_id)[0]
        resp = HttpResponse(content_type='application/pdf')
        return generate_pdf('peticions/juntes/render_pdf.html', file_object=resp, context={
                                                                            'junta_instance': junta_instance, 
                                                                            'issue_add_comments': False,
                                                                            'issue_title_size': 'h4',
                                                                            'user_admin': True,
                                                                            'is_pdf': True
                                                                        })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')


@user_passes_test(lambda u: u.is_staff)
def delete_comment(request, issue_id, comment_id):
    try:
        comment_instance = Comment.objects.filter(id=comment_id, issue__id=issue_id)[0]
       
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                comment_instance.delete()
                return redirect('peticions.edit.issue', {'issue_id': issue_id})
            else:
                messages.error(request, 'Error eliminant comentari')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'peticions/comments/delete.html', { 'comment': comment_instance })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.edit.issue', {'issue_id': issue_id})

@user_passes_test(lambda u: u.is_staff)
def delete_junta(request, junta_id):
    try:
        junta_instance = Junta.objects.filter(id=junta_id)[0]
       
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                junta_instance.delete()
                return redirect('peticions.list.juntes')
            else:
                messages.error(request, 'Error eliminant la junta')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'peticions/juntes/delete.html', { 
                                                                    'junta_instance': junta_instance,
                                                                    'issue_title_size': 'h4',
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')

@user_passes_test(lambda u: u.is_staff)
def delete_representant(request, representant_id):
    try:
        instance_representant = Representant.objects.filter(id=representant_id)[0]
       
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                instance_representant.delete()
                return redirect('peticions.list.representants')
            else:
                messages.error(request, 'Error eliminant representant')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'peticions/representants/delete.html', { 'instance_representant': instance_representant })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.representants')

@user_passes_test(lambda u: u.is_staff)
def delete_category(request, category_id):
    try:
        instance_category = Category.objects.filter(id=category_id)[0]
       
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                instance_category.delete()
                return redirect('peticions.list.categories')
            else:
                messages.error(request, 'Error eliminant la categoria')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'peticions/categories/delete.html', { 'instance_category': instance_category })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.categories')

@user_passes_test(lambda u: u.is_staff)
def delete_issue(request, issue_id):
    try:
        instance_issue = Issue.objects.filter(id=issue_id)[0]
       
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                instance_issue.delete()
                return redirect('peticions.list.issues')
            else:
                messages.error(request, 'Error eliminant la petició')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'peticions/issues/delete.html', { 'issue_instance': instance_issue })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.issues')

@user_passes_test(lambda u: u.is_staff)
def publish_junta(request, junta_id):
    try:
        junta_instance = Junta.objects.filter(id=junta_id)[0]
       
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                
                for issue in junta_instance.issues.all():
                    issue.status = ISSUE_STATUS_CLOSED
                    issue.save()
                junta_instance.public = True
                junta_instance.save()

                messages.info(request, 'Junta publicada')

                return redirect('peticions.list.juntes')
            else:
                messages.error(request, 'Error eliminant la junta')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'peticions/juntes/publish.html', { 
                                                                    'junta_instance': junta_instance,
                                                                    'issue_title_size': 'h4',
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')

@user_passes_test(lambda u: u.is_staff)
def edit_representant(request, representant_id=None):
    try:
        if representant_id:
            representant_instance = Representant.objects.filter(id=representant_id)[0]
        else:
            representant_instance = Representant()

        if request.method == 'POST':
            form = RepresentantForm(request.POST, instance=representant_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Representant guardat correctament')
                return redirect('peticions.list.representants')
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'peticions/representants/edit.html', { 
                                                        'form': form, 
                                                        'representant_instance': representant_instance, 
                                                    })
        else:
            form = RepresentantForm(instance=representant_instance)
            return render(request, 'peticions/representants/edit.html', { 
                                                                    'form': form, 
                                                                    'representant_instance': representant_instance, 
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.representants')

@user_passes_test(lambda u: u.is_staff)
def edit_category(request, category_id=None):
    try:
        if category_id:
            category_instance = Category.objects.filter(id=category_id)[0]
        else:
            category_instance = Category()

        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Categoria guardada correctament')
                return redirect('peticions.list.categories')
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'peticions/categories/edit.html', { 
                                                        'form': form, 
                                                        'category_instance': category_instance, 
                                                    })
        else:
            form = CategoryForm(instance=category_instance)
            return render(request, 'peticions/categories/edit.html', { 
                                                                    'form': form, 
                                                                    'category_instance': category_instance, 
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.categories')

@user_passes_test(lambda u: u.is_staff)
def list_categories(request):
    list_categories_raw = Category.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(list_categories_raw, 10)
    try:
        list_categories = paginator.page(page)
    except PageNotAnInteger:
        list_categories = paginator.page(1)
    except EmptyPage:
        list_categories = paginator.page(paginator.num_pages)

    return render(request, 'peticions/categories/list.html', {
                                                                'list_categories': list_categories, 
                                                                'public': False, 
                                                                'user_admin': request.user.is_staff
                                                            })

@user_passes_test(lambda u: u.is_staff)
def list_representants(request):
    list_representants_raw = Representant.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(list_representants_raw, 10)
    try:
        list_representants = paginator.page(page)
    except PageNotAnInteger:
        list_representants = paginator.page(1)
    except EmptyPage:
        list_representants = paginator.page(paginator.num_pages)

    return render(request, 'peticions/representants/list.html', {
                                                                'list_representants': list_representants, 
                                                                'public': False, 
                                                                'user_admin': request.user.is_staff
                                                            })

@user_passes_test(lambda u: u.is_staff)
def forward_open_peticions(request):
    try:
        list_issues = Issue.objects.filter(public=True, status=ISSUE_STATUS_DRAFT)
        config = Entitat.objects.first()

        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                for issue in list_issues:
                    issue.status = ISSUE_STATUS_OPEN
                    issue.save()
                messages.info(request, 'Canviat l\'estat de les peticions')
                return redirect('peticions.list.issues')    
            else:
                messages.error(request, 'Error fent el canvi d\'estat')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'peticions/issues/forward_open.html', {'list_issues': list_issues, 'config': config})
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.issues')       

@user_passes_test(lambda u: u.is_staff)
def edit_junta_peu(request, junta_id):
    try:
        junta_instance = Junta.objects.filter(id=junta_id)[0]

        if request.method == 'POST':
            form = JuntaPeuForm(request.POST, instance=junta_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Peu de junta guardat correctament')
                return redirect('peticions.edit.junta', junta_id=junta_id)
                
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'peticions/juntes/edit_peu.html', { 
                                                        'form': form, 
                                                        'junta_instance': junta_instance, 
                                                    })
        else:
            form = JuntaPeuForm(instance=junta_instance)
            return render(request, 'peticions/juntes/edit_peu.html', { 
                                                                    'form': form, 
                                                                    'junta_instance': junta_instance, 
                                                                })

    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.edit.junta', junta_id=junta_id)

@user_passes_test(lambda u: u.is_staff)
def edit_junta(request, junta_id=None):
    try:
        if junta_id:
            junta_instance = Junta.objects.filter(id=junta_id)[0]
        else:
            junta_instance = Junta()
        
        for categoria in junta_instance.categories:
            print(categoria)

        if request.method == 'POST':
            form = JuntaForm(request.POST, instance=junta_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Junta guardada correctament')
                try:
                    boto_apretat = str(form.data['votarem'])
                except:
                    try:
                        boto_apretat = str(form.data['queixarem'])
                        return redirect('peticions.edit.junta.list.peticions', junta_id=junta_instance.id)
                    except:
                        try:
                            boto_apretat = str(form.data['veure'])
                            return redirect('peticions.show.junta', junta_id=junta_instance.id)
                        except:
                            try:
                                boto_apretat = str(form.data['pudor'])
                                return redirect('peticions.edit.peu.junta', junta_id=junta_instance.id)
                            except:
                                try:
                                    boto_apretat = str(form.data['presentar'])
                                    return redirect('peticions.present.junta', junta_id=junta_instance.id)
                                except:
                                    pass
                return redirect('peticions.list.juntes')
                
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'peticions/juntes/edit.html', { 
                                                        'form': form, 
                                                        'junta_instance': junta_instance, 
                                                    })
        else:
            form = JuntaForm(instance=junta_instance)
            return render(request, 'peticions/juntes/edit.html', { 
                                                                    'form': form, 
                                                                    'junta_instance': junta_instance, 
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')

@user_passes_test(lambda u: u.is_staff)
def list_junta_peticio(request, junta_id):
    try:
        junta_instance = Junta.objects.filter(id=junta_id)[0]
        list_issues_add = Issue.objects.filter(public=True, status=ISSUE_STATUS_OPEN).exclude(id__in=junta_instance.issues.values('id'))

        list_issues_remove = junta_instance.issues.all()

        return render(request, 'peticions/juntes/add_to_junta_list.html', {
                                                                'list_issues_add': list_issues_add, 
                                                                'list_issues_remove': list_issues_remove, 
                                                                'public': False, 
                                                                'user_admin': request.user.is_staff,
                                                                'junta_instance': junta_instance
                                                            })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')

@user_passes_test(lambda u: u.is_staff)
def add_all_junta_peticio(request, junta_id):
    try:
        junta_instance = Junta.objects.filter(id=junta_id)[0]
       
        if request.method == 'POST':
            form = AreYouSureForm(request.POST)
            if form.is_valid():
                for issue in Issue.objects.filter(public=True, status=ISSUE_STATUS_OPEN):
                    issue.status = ISSUE_STATUS_WAITING
                    issue.save()
                    junta_instance.issues.add(issue)
                junta_instance.save()
                return redirect('peticions.edit.junta', junta_id=junta_id)
            else:
                messages.error(request, 'Error afegit peticions a la junta')
        else:
            form = AreYouSureForm(request.GET)
        return render(request, 'peticions/juntes/add_all_issues.html', { 'junta_instance': junta_instance, 'list_issues_add': Issue.objects.filter(public=True, status=ISSUE_STATUS_OPEN) })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')    

@user_passes_test(lambda u: u.is_staff)
def add_junta_peticio(request, junta_id, issue_id):
    try:
        if request.method == "POST":
            junta_instance = Junta.objects.filter(id=junta_id)[0]
            issue_instance = Issue.objects.filter(id=issue_id)[0]

            issue_instance.status = ISSUE_STATUS_WAITING
            issue_instance.save()

            junta_instance.issues.add(issue_instance)

            junta_instance.save()

    except Exception as e:
        messages.error(request, "Error afegint petició a l'ordre del dia")
        if request.user.is_superuser:
            messages.error(request, str(e))

    return redirect('peticions.edit.junta', junta_id=junta_id)    

@user_passes_test(lambda u: u.is_staff)
def remove_junta_peticio(request, junta_id, issue_id):
    try:
        if request.method == "POST":
            junta_instance = Junta.objects.filter(id=junta_id)[0]
            issue_instance = Issue.objects.filter(id=issue_id)[0]

            issue_instance.status = ISSUE_STATUS_OPEN
            issue_instance.save()

            junta_instance.issues.remove(issue_instance)

            junta_instance.save()

    except Exception as e:
        messages.error(request, "Error eliminant petició de l'ordre del dia")
        if request.user.is_superuser:
            messages.error(request, str(e))

    return redirect('peticions.edit.junta', junta_id=junta_id)    

# 
# registered
#

@user_passes_test(lambda u: u.is_staff)
def like_issue(request, issue_id):
    try:
        if request.method == "POST":
            issue_instance = Issue.objects.filter(id=issue_id)[0]

            if not request.user in issue_instance.likes.all():
                if request.user in issue_instance.dislikes.all():
                    issue_instance.dislikes.remove(request.user)
                    issue_instance.likes.add(request.user)
                else:
                    issue_instance.likes.add(request.user)
                issue_instance.save()

    except Exception as e:
        messages.error(request, "Error fent like")
        if request.user.is_superuser:
            messages.error(request, str(e))

    return redirect('peticions.show.issue', issue_id=issue_id)

@user_passes_test(lambda u: u.is_staff)
def dislike_issue(request, issue_id):
    try:
        if request.method == "POST":
            issue_instance = Issue.objects.filter(id=issue_id)[0]

            if not request.user in issue_instance.dislikes.all():
                if request.user in issue_instance.likes.all():
                    issue_instance.likes.remove(request.user)
                    issue_instance.dislikes.add(request.user)
                else:
                    issue_instance.dislikes.add(request.user)
                issue_instance.save()

    except Exception as e:
        messages.error(request, "Error fent dislike")
        if request.user.is_superuser:
            messages.error(request, str(e))

    return redirect('peticions.show.issue', issue_id=issue_id)

#
# login required
#

@login_required
def filter_issues(request):
    if request.method == 'POST':
        form = IssueFilterForm(request.POST)
        
        try:
            if form.data['status_filter'][0]:
                url = reverse('peticions.list.issues')
                return HttpResponseRedirect(url + "?status_filter="+form.data['status_filter'][0])
        except Exception as e:
            if request.user.is_superuser:
                messages.error(request, str(e))
            return redirect('peticions.list.issues')
    else:
        form = IssueFilterForm(request.GET)
        return render(request, 'peticions/issues/filter.html', {'form': form })

@login_required
def edit_comment(request, issue_id, comment_id=None):
    try:
        issue_instance = Issue.objects.filter(id=issue_id)[0]
        if issue_instance.status==ISSUE_STATUS_CLOSED:
            return redirect('peticions.edit.issue', issue_id=issue_id)
        if comment_id:
            comment_instance = Comment.objects.filter(issue__id=issue_id, id=comment_id)[0]
            is_new = False
        else:
            comment_instance = Comment(issue=Issue.objects.filter(id=issue_id)[0], user=request.user)
            is_new = True
        
        if is_new:
            if request.user.representant:
                comment_instance.representant=request.user.representant

        if request.method == 'POST':
            if request.user.is_staff:
                form = AdminCommentForm(request.POST, instance=comment_instance)
            else:
                form = CommentForm(request.POST, instance=comment_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Comentari guardat correctament')
                return redirect('peticions.edit.issue', issue_id=issue_id)
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'peticions/issues/edit.html', { 
                                                        'form': form, 
                                                        'comment_instance': comment_instance, 
                                                        'is_new': is_new,
                                                        'issue_id': issue_id,
                                                        'issue_instance': issue_instance,
                                                    })
        else:
            if request.user.is_staff:
                form = AdminCommentForm(instance=comment_instance)
            else:
                form = CommentForm(instance=comment_instance)
            return render(request, 'peticions/comments/edit.html', { 
                                                                    'form': form, 
                                                                    'comment_instance': comment_instance, 
                                                                    'is_new': is_new,
                                                                    'issue_id': issue_id,
                                                                    'issue_instance': issue_instance,
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.edit.issue', issue_id=issue_id)

@login_required
def show_issue(request, issue_id):
    try:
        config = Entitat.objects.first()
        issue_instance = Issue.objects.filter(id=issue_id)[0]
        return render(request, 'peticions/issues/show.html', { 
                                                'issue_instance': issue_instance,
                                                'config': config,
                                                'user_admin': request.user.is_staff,
                                                'issue_add_comments': True,
                                                'issue_title_size': 'h1'
                                            })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.issues')


@login_required
def edit_issue(request, issue_id=None):
    try:
        if issue_id:
            issue_instance = Issue.objects.filter(id=issue_id)[0]
            is_new = False
        else:
            issue_instance = Issue(owner=request.user)
            is_new = True

        if is_new:
            if request.user.representant:
                issue_instance.representant=request.user.representant

        if request.user==issue_instance.owner or request.user.is_staff:
            owner_view = True
        else:
            owner_view = False

        if issue_instance.owner!=request.user and not request.user.is_staff:
            return redirect('peticions.show.issue', issue_id=issue_id)

        if request.method == 'POST':
            if request.user.is_staff:
                form = IssueAdminForm(request.POST, instance=issue_instance)
            else:
                form = IssueForm(request.POST, instance=issue_instance)
            if form.is_valid():
                form.save()
                messages.info(request, 'Petició guardada correctament')
                return redirect('peticions.list.issues')
            else:
                messages.error(request, 'Formulari incorrecte')
                return render(request, 'peticions/issues/edit.html', { 
                                                        'form': form, 
                                                        'issue_instance': issue_instance, 
                                                        'is_new': is_new,
                                                        'owner_view': owner_view,
                                                        'user': request.user,
                                                        'user_admin': request.user.is_staff
                                                    })
        else:
            if request.user.is_staff:
                form = IssueAdminForm(instance=issue_instance)
            else:
                form = IssueForm(instance=issue_instance)
            return render(request, 'peticions/issues/edit.html', { 
                                                                    'form': form, 
                                                                    'issue_instance': issue_instance, 
                                                                    'is_new': is_new,
                                                                    'owner_view': owner_view,
                                                                    'user': request.user,
                                                                    'user_admin': request.user.is_staff
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.issues')

@login_required
def list_issues(request):
    config = Entitat.objects.first()

    issue_status = request.GET.get('status_filter', None)

    # print(str(issue_status))

    if request.user.is_staff:
        list_issues_raw = Issue.objects.all()
    else:
        list_issues_raw = Issue.objects.filter(public=True)

    # print(list_issues_raw.count())

    if issue_status:
        # print('applico filtre status')
        list_issues_raw = list_issues_raw.filter(status=issue_status)

    # print(list_issues_raw.count())

    page = request.GET.get('page', 1)
    paginator = Paginator(list_issues_raw, 10)
    try:
        list_issues = paginator.page(page)
    except PageNotAnInteger:
        list_issues = paginator.page(1)
    except EmptyPage:
        list_issues = paginator.page(paginator.num_pages)

    return render(request, 'peticions/issues/list.html', {
                                                            'list_issues': list_issues,
                                                            'config': config,
                                                            'public': False, 
                                                            'user_admin': request.user.is_staff,
                                                            'issue_status': issue_status
                                                        })

#
# PUBLIC
#

def list_juntes(request):
    user_admin = False
    if request.user.is_authenticated:
        if request.user.is_staff:
            user_admin = True
            list_juntes_raw = Junta.objects.all()
        else:
            list_juntes_raw = Junta.objects.filter(public=True)
    else:
        list_juntes_raw = Junta.objects.filter(public=True)

    page = request.GET.get('page', 1)

    paginator = Paginator(list_juntes_raw, 10)
    try:
        list_juntes = paginator.page(page)
    except PageNotAnInteger:
        list_juntes = paginator.page(1)
    except EmptyPage:
        list_juntes = paginator.page(paginator.num_pages)

    return render(request, 'peticions/juntes/list.html', {
                                                                'list_juntes': list_juntes,
                                                                'user_admin': user_admin
                                                            })

def present_junta(request, junta_id):
    try:
        user_admin = False
        if request.user.is_authenticated:
            if request.user.is_staff:
                user_admin = True
                junta_instance = Junta.objects.filter(id=junta_id)[0]
            else:
                junta_instance = Junta.objects.filter(id=junta_id, public=True)[0]
        else:
            junta_instance = Junta.objects.filter(id=junta_id, public=True)[0]

        return render(request, 'peticions/juntes/present.html', { 
                                                                'junta_instance': junta_instance, 
                                                                'issue_add_comments': False,
                                                                'issue_title_size': 'h4',
                                                                'user_admin': user_admin
                                                            })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')

def show_junta(request, junta_id):
    try:
        user_admin = False
        if request.user.is_authenticated:
            if request.user.is_staff:
                user_admin = True
                junta_instance = Junta.objects.filter(id=junta_id)[0]
            else:
                junta_instance = Junta.objects.filter(id=junta_id, public=True)[0]
        else:
            junta_instance = Junta.objects.filter(id=junta_id, public=True)[0]

        return render(request, 'peticions/juntes/show.html', { 
                                                                'junta_instance': junta_instance, 
                                                                'issue_add_comments': False,
                                                                'issue_title_size': 'h4',
                                                                'user_admin': user_admin
                                                            })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')

def show_acte_junta(request, junta_slug):
    try:
        junta_instance = Junta.objects.filter(slug=junta_slug)[0]

        return show_junta(request, junta_instance.id)
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.juntes')