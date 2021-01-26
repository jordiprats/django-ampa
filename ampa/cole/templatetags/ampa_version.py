from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

import os

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def ampa_version(value):
    return os.getenv('AMPA_APP_VERSION', '3.14159265359')