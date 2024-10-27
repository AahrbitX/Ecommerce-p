from django.contrib.auth import authenticate
from common.serializers import *
from rest_framework.exceptions import ValidationError

class CustomUserHandler:
  
  def signup_user(data):
    serializer = SignupSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return user
    else:
        raise ValidationError(serializer.errors)