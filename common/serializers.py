from rest_framework import serializers
from common.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=CustomUser

        fields=['username','mobile_number','password']

        extra_kwargs = {'password': {'write_only': True}}


    
    def create(self, validated_data):
        user = CustomUser(**validated_data)

        mobile_number=self.validated_data['mobile_number']

        verify_mobile = CustomUser.objects.filter(mobile_number=mobile_number).exists()


        if verify_mobile:

                raise serializers.ValidationError('Mobile Number already exists')
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
     
      
    mobile_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)