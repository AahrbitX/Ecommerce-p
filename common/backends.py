from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
import logging
 

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Check if email and password are provided
        if not email or not password:
            
            return None

        try:
            # Attempt to retrieve the user by email
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
           
            return None

        # Check password validity and if the user is active
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

         
        return None

    def user_can_authenticate(self, user):
        return user.is_active

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            
            return None
