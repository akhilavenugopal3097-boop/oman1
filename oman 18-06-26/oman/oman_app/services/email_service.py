import random
from django.core.mail import send_mail
from django.conf import settings

class EmailOTPService:
    @staticmethod
    def generate_otp():
        return random.randint(100000, 999999)

    @staticmethod
    def send_otp(email, otp):
        subject = "Your Verification Code"
        message = f"Your OTP for account verification is: {otp}\nIt expires in 5 minutes."
        from_email = settings.DEFAULT_FROM_EMAIL
        try:
            send_mail(subject, message, from_email, [email])
            return True, {"message": "OTP sent"}
        except Exception as e:
            return False, {"error": str(e)}