from django.template.defaultfilters import stringfilter
from django.utils.text import slugify
from django import template

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def slugify(value):
    return slugify(value)