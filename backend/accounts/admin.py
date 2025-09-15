from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Plan", {"fields": ("plan",)}),)
    list_display = ("username", "email", "plan", "is_staff", "is_active")


admin.site.register(User, CustomUserAdmin)
