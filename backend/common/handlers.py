from django.contrib.auth import authenticate
from common.serializers import *
from rest_framework.exceptions import ValidationError
import random
import string
from django.core.mail import send_mail
from root.settings import EMAIL_HOST_USER
import time
from rest_framework.response import Response

import hashlib
from datetime import  timedelta
from django.utils import timezone 
from django.utils.timezone import now
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
import logging
import traceback
from django.template.exceptions import TemplateDoesNotExist


logger = logging.getLogger(__name__)
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
    # OTP_MAX_ATTEMPTS = 3
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

       
        # otp_attempts = OTPModel.objects.filter(user=user, created_at__gt=timezone.now() - ResetPasswordHandler.OTP_EXPIRATION_TIMEFRAME)
                                                          #otpcheck greater than created time      ->       #currenttime - 30 minutes  = check for last 30 minutes to evaluate 3 attempts
        # if otp_attempts >= ResetPasswordHandler.OTP_MAX_ATTEMPTS:
        #     raise ValidationError(f"Too many OTP requests. Please try again later.")
        
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
     

class VendorApplicationHandler:
    def __init__(self, application=None, data=None):
        self.application = application
        self.data = data

    def send_status_email(self, template_name, context, subject, recipient_email):
        try:
            # Render the email body using the specified template and context
            email_body = render_to_string(template_name, context)
            logger.info(f"Email body rendered successfully for template '{template_name}'.")

            # Construct and send the email
            email = EmailMessage(
                subject=subject,
                body=email_body,
                from_email=EMAIL_HOST_USER,
                to=[recipient_email],
            )
            email.content_subtype = "html"  # Set the email format to HTML
            email.send(fail_silently=False)
            logger.info(f"Email sent successfully to '{recipient_email}'.")
        except TemplateDoesNotExist as e:
            # Handle missing template exception
            logger.error(f"Template '{template_name}' not found. Verify the path and TEMPLATES settings.")
            raise ValidationError({
                "detail": "Template not found.",
                "error": str(e)
            })
        except Exception as e:
            # Catch all other exceptions
            error_details = traceback.format_exc()
            logger.error(f"Error sending email: {error_details}")
            raise ValidationError({
                "detail": "Failed to send email.",
                "error": str(e)
            })

    def validate_store_data(self):
        user = self.data.get("user_id")
        store_name = self.data.get('store_name')
        store_address = self.data.get('store_address')
        contact_number = self.data.get('contact_number')
        
        if not user:
            raise ValidationError({
                "error": "user_id not provided"
            })
        user = get_object_or_404(CustomUser, user_id=user)

        if not store_name or not store_address or not contact_number:
            raise ValidationError({
                "error": "missing_store_details"
            })
        return user, store_name, store_address, contact_number

    def create_vendor_application(self):
        user, store_name, store_address, contact_number = self.validate_store_data()
        self.application = VendorApplication.objects.create(
            user=user,
            application_status='pending',
            applied_on=now()
        )

        # Create VendorStore
        VendorStore.objects.create(
            user=user,
            application=self.application,
            store_name=store_name,
            store_address=store_address,
            contact_number=contact_number,
            established_on=now()
        )

        return "Vendor application and store created successfully.", self.application.vendor_application_id

    def validate_application_status(self, allowed_statuses):
        if self.application.application_status not in allowed_statuses:
            raise ValidationError({
                "detail": f"Invalid application status: {self.application.application_status}.",
                "error": "invalid_application_status"
            })

    def approve_application(self):
        try:
            if self.application.application_status == "approved":
                raise ValidationError({
                    "detail": "Application is already approved.",
                })
            self.application.application_status = 'approved'
            self.application.reviewed_on = now()
            user = self.application.user
             
            vendor_role = get_object_or_404(Role, name="vendor")
            if user.role != vendor_role:
                user.role = vendor_role
                user.save()

            self.application.save()

            subject = "Your Vendor Application Has Been Approved"
            context = {'user': user}
            self.send_status_email(
                subject=subject,
                template_name="vendor_approval.html",
                context=context,
                recipient_email=user.email,
            )
            return "Application approved successfully."
        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"Error approving application: {error_details}")
            raise ValidationError({
                "detail": "An error occurred while approving the application.",
                "error": str(e)
            })

    def validate_rejection(self):
        if self.application.application_status == 'rejected':
            raise ValidationError({
                "detail": "Application is already rejected.",
            })
        if self.application.application_status == 'approved':
            raise ValidationError({
                "detail": "Approved applications cannot be rejected.",
                "error": "approved_application_rejection"
            })

    def reject_application(self, rejection_reason):
        self.validate_rejection()
        if not rejection_reason:
            raise ValidationError({
                "detail": "Rejection reason is required.",
            })
        self.application.application_status = 'rejected'
        self.application.rejection_reason = rejection_reason
        self.application.reviewed_on = now()
        self.application.save()

        user = self.application.user

        enduser_role = get_object_or_404(Role, name="end_user")
        if user.role != enduser_role:
            user.role = enduser_role
            user.save()

        subject = "Your Vendor Application Has Been Rejected"
        context = {'user': user}
        self.send_status_email(
            subject=subject,
            template_name="vendor_rejection.html",
            context=context,
            recipient_email=user.email,
        )
        return "Application rejected successfully."
