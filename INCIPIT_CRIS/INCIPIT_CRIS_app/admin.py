from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Title, User

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'pid', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'pid')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


    list_display = ['pid', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

    def __init__(self, *args, **kwargs):
        super(BaseUserAdmin,self).__init__(*args, **kwargs)
        BaseUserAdmin.list_display = list(BaseUserAdmin.list_display)

admin.register(UserAdmin)
admin.site.register(Title)