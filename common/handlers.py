from django.contrib.auth import authenticate
from common.serializers import *
from rest_framework.exceptions import ValidationError
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from root.settings import EMAIL_HOST_USER
import time
from rest_framework.response import Response
class CustomUserHandler:
  
  def signup_user(data):
    serializer = SignupSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return user
    else:
        raise ValidationError(serializer.errors)
    
def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    characters = string.digits  # OTP usually contains digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_email(recipient_email):
    """Generate OTP and send it via email."""
    otp = generate_otp()

    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp}"
    sender_email = EMAIL_HOST_USER
    try:
        send_mail(
            subject,
            message,
            sender_email,
            [recipient_email],
            fail_silently=False,
        )
        print(f"OTP sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending OTP: {e}")

    return otp
class ResetPasswordHandler:
   
    @staticmethod
    def forgot_password(request):
        try:
            email = request.data.get('email')

            if not email:
                raise ValidationError("Email is required.")
   
            user_obj = CustomUser.objects.filter(email=email).first()
            if not user_obj:
                raise ValidationError("Email does not exist. Please try again with a valid email.")

            otp = send_otp_email(email)

            request.session['otp'] = otp
            request.session['otp_timestamp'] = time.time()   
            request.session['email'] = email

            return  "OTP sent successfully to your email."

        except ValidationError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=500
            )

    @staticmethod
    def verify_otp(request):
        try:
            user_input_otp = request.data.get('otp')
            reset_password = request.data.get('new_password')

            session_otp = request.session.get('otp')
            otp_timestamp = request.session.get('otp_timestamp')
            session_email = request.session.get('email')

            if not session_otp or not otp_timestamp:
                raise ValidationError("OTP has expired or was not generated.")

            current_time = time.time()
            otp_age = current_time - otp_timestamp
            if otp_age > 300:  # 300 seconds = 5 minutes
                raise ValidationError("OTP has expired, please request a new one.")

            if user_input_otp != session_otp:
                raise ValidationError("Invalid OTP, please try again.")

            if not reset_password:
                raise ValidationError("Password is required.")

            user_obj = CustomUser.objects.filter(email=session_email).first()
            if not user_obj:
                raise ValidationError("User does not exist.")

            user_obj.set_password(reset_password)
            user_obj.save()

            request.session.pop('otp', None)
            request.session.pop('otp_timestamp', None)
            request.session.pop('email', None)

            return Response({"message": "Password has been reset successfully."}, status=200)

        except ValidationError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
 