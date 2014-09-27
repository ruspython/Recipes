from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def split(value, cut):
    return value.split(cut, 1)[0]


@register.filter()
@stringfilter
def delete_cuts(value, cut):
    return value.replace(cut, "")