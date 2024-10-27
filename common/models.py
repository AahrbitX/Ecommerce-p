from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, mobile_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        
        user = self.model(
            email=self.normalize_email(email),
            mobile_number=mobile_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password=None):
        user = self.create_user(
            email,
            password=password,
            mobile_number=mobile_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username=models.CharField(max_length=400,verbose_name='UserName')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
