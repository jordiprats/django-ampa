from django.template.defaultfilters import stringfilter
from django.db.models import Count
from django import template

from peticions.models import *
from cole.models import *

import markdown as md

import os

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def issues_filter_by_category(category_id, results):
    category_instance = Category.objects.filter(id=category_id).first()
    return results.annotate(cat_count=Count('categories')).filter(cat_count=1).filter(categories=category_instance)