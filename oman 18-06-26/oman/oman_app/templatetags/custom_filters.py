# oman_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """Replaces all occurrences of a substring with another.
    Usage: {{ value|replace:"old,new" }}
    """
    if not value:
        return value
    try:
        old, new = arg.split(',')
        return str(value).replace(old, new)
    except (ValueError, TypeError):
        return value

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key"""
    return dictionary.get(key)