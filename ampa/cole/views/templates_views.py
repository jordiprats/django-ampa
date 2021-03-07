from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages

from cole.forms import *

import sys
import os

@user_passes_test(lambda u: u.is_staff)
def list_templates(request):
    list_templates = DocumentTemplate.objects.all()
    return render(request, 'templates/list.html', {
                                                                'list_templates': list_templates, 
                                                            })