from rest_framework import serializers
from common.models import *

 

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ['user_id', 'email', 'mobile_number', 'password','username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

  
# class LoginSerializer(serializers.Serializer):
#     email_or_mobile = serializers.CharField(max_length=300)   
#     password = serializers.CharField(write_only=True)