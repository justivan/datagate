from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = (
        "username",
        "name",
        "designation",
        "email",
        "last_login",
        "is_superuser",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Information", {"fields": ("name", "email")}),
        ("Additional Information", {"fields": ("designation",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ("name", "email")
