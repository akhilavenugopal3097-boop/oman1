# app/templatetags/querystring.py
from django import template

register = template.Library()

@register.simple_tag
def param_replace(request, **kwargs):
    """
    Replace or remove query parameters while preserving others.
    Handles both single and multiple values.
    """
    params = request.GET.copy()

    for key, value in kwargs.items():
        if value is None:
            # remove parameter completely
            params.pop(key, None)
        elif isinstance(value, list):
            # set multiple values properly
            params.setlist(key, value)
        else:
            # overwrite normally
            params[key] = value

    return params.urlencode()
