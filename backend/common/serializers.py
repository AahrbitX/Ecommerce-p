from rest_framework import serializers
from common.models import *

# class CustomUserSerializer(serializers.Serializer):
#     class Meta:
#         model = CustomUser
#         fields = ['email','password']

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'profile_picture', 'bio', 'phone_number']

    def update(self, instance, validated_data):
        """
        Update the user profile with new data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
