from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])