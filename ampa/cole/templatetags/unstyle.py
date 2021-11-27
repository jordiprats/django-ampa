from django.template.defaultfilters import stringfilter
from django import template

import re

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def unstyle(input_string):  
    return re.sub("style=\"[^\"]+\"", "", input_string)