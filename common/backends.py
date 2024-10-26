from django.contrib.auth.backends import BaseBackend
from common.models import CustomUser

class MobileBackend(BaseBackend):
    def authenticate(self, request, username=None, mobile_number=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(mobile_number=mobile_number)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None   
        except Exception as e: 
            print(f"Error in authentication: {str(e)}")
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return None
