# oman_app/templatetags/chat_filters.py
from django import template

register = template.Library()

@register.filter
def get_by_id(queryset, id):
    """
    Get an object from a queryset by its ID.
    """
    try:
        return queryset.get(id=id)
    except:
        return None

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary by key.
    """
    return dictionary.get(key, None)

@register.filter
def has_chat_with(user1, user2):
    """
    Check if user1 has any chats with user2.
    """
    from oman_app.models import ChatMessage
    return ChatMessage.objects.filter(
        Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)
    ).exists()