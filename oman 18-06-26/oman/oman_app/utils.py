# utils.py or views.py

import re

def normalize_phone(phone):
    """
    Normalize phone number to Oman format (+968XXXXXXXX)
    Accepts formats:
    - 91234567 (local)
    - 091234567 (with leading zero)
    - 96891234567 (without +)
    - +96891234567 (international)
    """
    if not phone:
        return None
    
    # Remove all non-digit characters
    phone = re.sub(r'[^\d+]', '', phone.strip())
    
    # Remove leading '0' if present (Oman local numbers start with 0)
    if phone.startswith('0'):
        phone = phone[1:]
    
    # If it already starts with +968, return as is
    if phone.startswith('+968'):
        return phone
    
    # If it starts with 968 (without +), add the +
    if phone.startswith('968'):
        return '+' + phone
    
    # For local numbers (7-8 digits), add +968
    # Oman mobile numbers are typically 8 digits starting with 9, 7, etc.
    if len(phone) >= 7 and len(phone) <= 8:
        return '+968' + phone
    
    # Fallback - just add +968
    return '+968' + phone

# Example usage:
# normalize_phone("91234567") -> "+96891234567"
# normalize_phone("091234567") -> "+96891234567"
# normalize_phone("96891234567") -> "+96891234567"
# normalize_phone("+96891234567") -> "+96891234567"


# utils.py or views.py

from django.utils import timezone
from .models import RecentlyViewed

def track_recently_viewed(request, content_type, object_id, category, ad_data=None):
    """Track recently viewed items for authenticated users"""
    
    if request.user.is_authenticated:
        # Get or create the recently viewed record
        recent, created = RecentlyViewed.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            defaults={
                'category': category,
                'viewed_at': timezone.now()
            }
        )
        
        if not created:
            # Update the viewed_at time
            recent.viewed_at = timezone.now()
            recent.save()
        
        # Keep only last 20 items per user
        recent_items = RecentlyViewed.objects.filter(user=request.user)
        if recent_items.count() > 5:
            recent_items.last().delete()
        
        return True
    return False