from django.template.defaultfilters import stringfilter
from django import template

from cole.models import *

import markdown as md

import os

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def ampa_title(value):
    try:
        entitat_instance = Entitat.objects.all()[0]
        if entitat_instance.name:
            entitat_name = str(entitat_instance.name)
        else:
            entitat_name = ""
        
        if entitat_instance.logo:
            desired_protocol =  os.getenv('PROTOCOL', 'http')   
            return "<img src='"+re.sub('^http://', desired_protocol+'://', entitat_instance.logo.static_url)+"'>"+str(entitat_name)
        else:
            return str(entitat_name)
    except Exception as e:
        print(str(e))
        return ""