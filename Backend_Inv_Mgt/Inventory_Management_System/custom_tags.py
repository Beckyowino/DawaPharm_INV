from django import template

register = template.Library()

@register.simple_tag
def is_active(request, *args):
    if request.path in args:
        return 'active'
    return ''
