from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        try:
            role = Role.objects.get(name='super_user')   
        except Role.DoesNotExist:
            raise ValueError('The role "super_user" does not exist in the Role table.')

        user = self.create_user(
            email=email,
            password=password,
            role=role
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Role(models.Model):
    ROLE_CHOICES = (
        ('super_user', 'SuperUser'),
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('end_user', 'EndUser'),
    )
    name = models.CharField(max_length=50, unique=True, default="end_user", choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)   
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)   
    created_at = models.DateField(auto_now_add=True, null=True)  

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """Grant admin access based on is_superuser."""
        return self.is_superuser
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
         return self.name if self.name else f"UserProfile for {self.user.email}"
class OTPModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField() 
  
class VendorApplication(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="vendor_application")
    vendor_application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_on = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True) 

    def __str__(self):
        return f"{self.user.email} - {self.application_status}"

# Vendor Store Model
class VendorStore(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="vendor_store")
    application = models.OneToOneField(VendorApplication, on_delete=models.CASCADE, related_name="vendor_store")
    store_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store_name = models.CharField(max_length=100)
    store_address = models.TextField()
    contact_number = models.CharField(max_length=15)
    established_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Store: {self.store_name} - Owner: {self.user.email}"