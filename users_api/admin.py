from django.contrib import admin
from users_api import models
# Register your models here.

admin.site.register(models.UserModel)
admin.site.register(models.MessageItem)
