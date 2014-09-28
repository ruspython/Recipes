from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

CUT = '&lt;cut&gt;'

@register.filter()
@stringfilter
def split(value):
    return value.split(CUT, 1)[0]


@register.filter()
@stringfilter
def delete_cuts(value):
    return value.replace(CUT, "")


@register.filter()
@stringfilter
def allow_code(value):
    pattern = re.compile('\[code\]', re.IGNORECASE)
    value = pattern.sub('<pre><code>', value)
    pattern = re.compile('\[/code\]', re.IGNORECASE)
    value = pattern.sub('</pre></code>', value)
    return value

@register.filter()
def nothing(value):
    return value.replace('[cut]', '')