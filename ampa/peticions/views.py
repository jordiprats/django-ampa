from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from peticions.models import *
from peticions.forms import *

#
# staff
#
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
    list_categories = Category.objects.all()
    return render(request, 'peticions/categories/list.html', {
                                                                'list_categories': list_categories, 
                                                                'public': False, 
                                                                'user_admin': request.user.is_staff
                                                            })


# 
# registered
#

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

        if request.method == 'POST':
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
        issue_instance = Issue.objects.filter(id=issue_id)[0]
        return render(request, 'peticions/issues/show.html', { 
                                                'issue_instance': issue_instance,
                                                'user_admin': request.user.is_staff
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
                                                        'user': request.user
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
                                                                    'user': request.user
                                                                })
    except Exception as e:
        if request.user.is_superuser:
            messages.error(request, str(e))
        return redirect('peticions.list.issues')

@login_required
def list_issues(request):
    if request.user.is_staff:
        list_issues = Issue.objects.all()        
    else:
        list_issues = Issue.objects.filter(public=True)
    return render(request, 'peticions/issues/list.html', {
                                                            'list_issues': list_issues, 
                                                            'public': False, 
                                                            'user_admin': request.user.is_staff
                                                        })

#
# PUBLIC
#

def list_juntes(request):
    user_admin = False
    if request.user.is_authenticated:
        if request.user.is_staff:
            user_admin = True
    list_juntes = Junta.objects.all()
    return render(request, 'peticions/juntes/list.html', {
                                                                'list_juntes': list_juntes,
                                                                'user_admin': user_admin
                                                            })