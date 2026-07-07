from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def product_view_count(context, obj):
    request = context['request']
    key = f'viewed_{request.user.id}_{obj._meta.model_name}_{obj.id}'
    return 1 if request.session.get(key) else 0
