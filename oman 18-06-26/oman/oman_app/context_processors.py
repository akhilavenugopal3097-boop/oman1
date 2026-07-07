from .models import ChatMessage

def unread_chat_count(request):
    if request.user.is_authenticated:
        count = ChatMessage.objects.filter(
            receiver=request.user,
            is_read=False,
            is_admin_chat=False
        ).count()
    else:
        count = 0

    return {'total_unread_chats': count}

from .models import JobCategory

def job_categories_processor(request):
    categories = list(JobCategory.objects.all())

    half = (len(categories) + 1) // 2

    return {
        'job_categories_left': categories[:half],
        'job_categories_right': categories[half:]
    }