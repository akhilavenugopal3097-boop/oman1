import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class SMSService:

    @staticmethod
    def send_sms(phone, message):
        """
        Send SMS using iSmartSMS API
        """

        # 🧪 Development mode (no real SMS sent)
        if settings.DEBUG:
            print("\n" + "=" * 50)
            print(f"[SMS DEBUG] To: {phone}")
            print(f"[SMS DEBUG] Message: {message}")
            print("=" * 50 + "\n")

            logger.info(f"DEV MODE: SMS to {phone}: {message}")
            return True, {"message": "Development mode - SMS simulated"}

        try:
            success, result = SMSService._send_via_ismart_api(phone, message)

            if success:
                logger.info("SMS sent successfully via iSmartSMS")
                return True, result
            else:
                logger.error(f"SMS failed: {result.get('error')}")
                return False, result

        except Exception as e:
            logger.error(f"SMS Exception: {str(e)}")
            return False, {"error": str(e)}

    @staticmethod
    def _send_via_ismart_api(phone, message):
        """
        Send SMS using iSmartSMS HTTP POST API
        """

        url = settings.ISMS_BASE_URL

        # Remove '+' if exists
        clean_phone = phone.replace('+', '')

        payload = {
            "UserId": settings.ISMS_USERNAME,
            "Password": settings.ISMS_PASSWORD,
            "MobileNo": clean_phone,
            "Message": message,
            "Lang": "0",
            "Header": settings.ISMS_SENDER_ID,
        }

        try:
            response = requests.post(url, data=payload, timeout=15)

            print("\n--- SMS API DEBUG ---")
            print("URL:", url)
            print("PAYLOAD:", payload)
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)
            print("---------------------\n")

            if response.status_code == 200:
                response_text = response.text.strip()

                if response_text == "1":
                    return True, {"message": "SMS sent successfully"}

                return False, {"error": f"API Error Code: {response_text}"}

            return False, {"error": f"HTTP {response.status_code}"}

        except Exception as e:
            return False, {"error": str(e)}

    @staticmethod
    def send_otp(phone, otp):
        """
        Send OTP message
        """
        message = f"Your OMAN DEAL verification code is: {otp}. Valid for 5 minutes."
        return SMSService.send_sms(phone, message)