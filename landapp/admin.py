from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Customize the admin options here if needed
    pass

admin.site.register(User, CustomUserAdmin)
