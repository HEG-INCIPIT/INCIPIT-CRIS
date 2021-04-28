from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'ark_pid', 'password1', 'password2')
        }),
    )

    list_display = ['ark_pid', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
