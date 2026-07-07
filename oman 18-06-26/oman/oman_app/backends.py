# oman_app/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class UsernameOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        # If the input is exactly 8 digits, prepend +968
        if username.isdigit() and len(username) == 8:
            username = '+968' + username
        
        # Try username first
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Then try phone (which now may include +968)
            try:
                user = User.objects.get(phone=username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None