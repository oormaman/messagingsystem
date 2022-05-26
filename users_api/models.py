from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings

class UserModelManager(BaseUserManager):
    """Manager for users"""
    def create_user(self, email,password ,name):
        """Create a new user"""
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user=self.model(email=email,name=name)
        # Password encryption
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password,name):
        """Create a new superuser"""
        user = self.create_user(email,password,name)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user
# Create your models here.
class UserModel(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserModelManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email

class MessageItem(models.Model):
    """Message Item"""
    sender_id = models.CharField(max_length=255)
    recipient_id = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    recipient_of_the_message_read_it=models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.message
    def get_sender_id(self):
        return self.sender_id
    def get_recipient_id(self):
        return self.recipient_id