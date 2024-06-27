from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "last_login",
        "date_joined",
        "is_active",
        "is_staff"
    ]
    search_fields = ("email", "username", "first_name", "last_name",)


admin.site.register(User, UserAdmin)
