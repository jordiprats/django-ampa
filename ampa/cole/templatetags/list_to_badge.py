from django.template.defaultfilters import stringfilter
from django import template

from cole.models import *

import markdown as md

import os

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def list_to_badge(tipus, items):
    ret_str = ""
    for item in items:
        ret_str += "<span class=\"badge badge-"+tipus+"\">"+str(item)+"</span> "
    return ret_str