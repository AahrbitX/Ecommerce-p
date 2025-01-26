from rest_framework import serializers
from common.models import *

# class CustomUserSerializer(serializers.Serializer):
#     class Meta:
#         model = CustomUser
#         fields = ['email','password']

class UserRoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Role
        fields = ['name']


class SignupSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False, default='end_user')

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role_name = validated_data.pop('role', 'end_user')
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            raise serializers.ValidationError(f'The role "{role_name}" does not exist.')

        user = CustomUser(
            role=role,
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

class VendorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorApplication
        fields = ['vendor_application_id', 'user', 'application_status', 'applied_on', 'reviewed_on']
        read_only_fields = ['application_status', 'applied_on', 'reviewed_on']


class VendorStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorStore
        fields = ['store_id', 'user', 'application', 'store_name', 'store_address', 'contact_number', 'established_on']
        read_only_fields = ['established_on']