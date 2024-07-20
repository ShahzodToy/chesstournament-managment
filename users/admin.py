from django.contrib import admin
from .models import User,UserConfirmation


admin.site.register(UserConfirmation)

class AdminUser(admin.ModelAdmin):
    list_display = ['id',"username",'email','phone_number']

admin.site.register(User,AdminUser)