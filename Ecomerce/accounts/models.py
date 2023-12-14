from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
      if not email:
          raise ValueError('The Email field must be set')
      email = self.normalize_email(email)
      user = self.model(email=email, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, password=None, **extra_fields):
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)
      return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
  name = models.CharField(max_length=30)
  email = models.EmailField(unique=True)
  phone_number = models.CharField(max_length=15, blank=True)
  otp_secret_key = models.CharField(max_length=50, default=False) # Add this line for the secret key
  otp = models.IntegerField(blank=True, null=True) 
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']

  def __str__(self):
      return self.email
