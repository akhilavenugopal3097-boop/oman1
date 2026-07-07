from django import template
from oman_app.models import ChatMessage

register = template.Library()

@register.filter
def has_chat_with(user, other_user):
    return ChatMessage.objects.filter(
        sender=user, receiver=other_user
    ).exists() or ChatMessage.objects.filter(
        sender=other_user, receiver=user
    ).exists()
