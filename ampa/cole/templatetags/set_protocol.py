from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

import os
import re

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def set_protocol(value):
    desired_protocol =  os.getenv('PROTOCOL', 'http')

    return re.sub('^http://', desired_protocol+'://', value)