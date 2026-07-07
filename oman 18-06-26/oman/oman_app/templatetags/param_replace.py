from django import template

register = template.Library()

@register.simple_tag
def param_replace(request, **kwargs):
    params = request.GET.copy()
    for key, value in kwargs.items():
        params[key] = value
    return params.urlencode()
