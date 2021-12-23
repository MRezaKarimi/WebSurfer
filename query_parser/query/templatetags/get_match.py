from django.utils.safestring import mark_safe
from django import template
from django.utils.text import Truncator
import re

register = template.Library()

@register.filter(is_safe=True)
def get_match(value: str, arg: str):
    query = arg.strip()
    match = re.search(query, value)
    if len(value) < 200:
        return value
    if match is None:
        return Truncator(value).words(40)
    else:
        index = match.start()
        rendered = \
            value[value.index(' ', index-150):index] + \
            '<span class="serp__match">' + \
            value[index:index+len(query)] + \
            ' </span>' + \
            Truncator(value[index+len(query):]).words(20)
        return mark_safe(rendered)