from django import template

register = template.Library()

@register.filter
def exclude(values, item):
    """
    Remove a single item from a list of values.
    Usage: values|exclude:"item"
    """
    return [v for v in values if v != item]
