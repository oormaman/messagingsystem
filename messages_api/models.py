from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
# from django.conf import settings
# from users_api import UserModel
# from
# Create your models here.
# class MessageItem(models.Model):
#     """Message Item"""
#     sender = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     recipient=models.ForeignKey(UserModel, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=255)
#     message = models.CharField(max_length=255)
#     recipient_of_the_message_read_it=models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         """Return the model as a string"""
#         return self.message
