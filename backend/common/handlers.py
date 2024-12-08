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
import secrets
import hashlib
from datetime import  timedelta
from django.utils import timezone 
class CustomUserHandler:
  
  def signup_user(data):
    serializer = SignupSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return user
    else:
        raise ValidationError(serializer.errors)

'''Dedicated class to handle only Password reset in case user forgot'''
class ResetPasswordHandler:
    OTP_EXPIRATION_MINUTES  = 5
    OTP_MAX_ATTEMPTS = 3
    OTP_EXPIRATION_TIMEFRAME = timedelta(minutes=30)
    
    @staticmethod
    def generate_otp(length=6):
        otp = ''.join(random.choices('0123456789', k=length))
        return otp
    
    @staticmethod
    def hash_otp(otp):
        # Hash the OTP using SHA-256 (this adds a layer of security by never storing plain OTP)
        return hashlib.sha256(otp.encode()).hexdigest()
  
    @staticmethod
    def send_otp_email(recipient_email, otp):
      
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
   
       
    
    @staticmethod
    def forgot_password(request):
        email = request.data.get('email')
        if not email:
            raise ValidationError("Email is required.")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError("User with this email does not exist.")

       
        otp_attempts = OTPModel.objects.filter(user=user, created_at__gt=timezone.now() - ResetPasswordHandler.OTP_EXPIRATION_TIMEFRAME).count()
                                                          #otpcheck greater than created time      ->       #currenttime - 30 minutes  = check for last 30 minutes to evaluate 3 attempts
        if otp_attempts >= ResetPasswordHandler.OTP_MAX_ATTEMPTS:
            raise ValidationError(f"Too many OTP requests. Please try again later.")
        
        otp = ResetPasswordHandler.generate_otp()
        otp_hash = ResetPasswordHandler.hash_otp(otp)   

        expiration_time = timezone.now() + timedelta(minutes=ResetPasswordHandler.OTP_EXPIRATION_MINUTES)
        OTPModel.objects.create(
            user=user,otp_hash=otp_hash,
                expiration_time=expiration_time,
        )
        ResetPasswordHandler.send_otp_email(email, otp)

        return {"message": "OTP has been sent successfully."}
   
    @staticmethod
    def verify_otp(request):
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not otp:
            raise ValidationError("OTP is required.")
        if not new_password:
            raise ValidationError("New password is required.")
        try:
            otp_hash = ResetPasswordHandler.hash_otp(otp)
            otp_record = OTPModel.objects.get(otp_hash=otp_hash)
        except OTPModel.DoesNotExist:
            raise ValidationError("Invalid OTP.")
        
        if timezone.now() > otp_record.expiration_time:
            raise ValidationError("OTP has expired.")

        # if otp_record.ip_address != request.META.get('REMOTE_ADDR'):
        #     raise ValidationError("Invalid OTP request source. IP address mismatch.")
 
        user = otp_record.user
        user.set_password(new_password)
        user.save()

        otp_record.delete()

        return {"message": "Password reset successfully."}