from django import template

register = template.Library()

@register.filter
def lower_model_name(obj):
    """Return the lowercased name of the object's model class."""
    return obj.__class__.__name__.lower()