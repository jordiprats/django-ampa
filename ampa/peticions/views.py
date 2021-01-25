from django.shortcuts import render, redirect
from django.contrib import messages

from peticions.models import *

# 
# PUBLIC
#

def list_issues(request):
    try:
        if request.user.is_staff:
            list_issues = Issue.objects.all()
            return render(request, 'peticions/issues/list.html', {'list_issues': list_issues, 'public': False, 'user_admin': request.user.is_staff })
    except:
        pass

    list_issues = Issue.objects.filter(public=True)
    return render(request, 'peticions/issues/list.html', {'list_issues': list_issues, 'public': True, 'user_admin': request.user.is_staff })
