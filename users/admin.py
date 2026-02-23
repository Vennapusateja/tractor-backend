from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ['name', 'phone', 'role', 'verified', 'is_active', 'created_at']
    list_filter   = ['role', 'verified', 'is_active', 'state']
    search_fields = ['name', 'phone', 'email']
    ordering      = ['-created_at']

    fieldsets = (
        ('Identity',      {'fields': ('name', 'phone', 'email', 'password')}),
        ('Profile',       {'fields': ('role', 'profile_photo', 'location', 'state', 'district', 'pincode')}),
        ('Verification',  {'fields': ('verified', 'aadhaar_number')}),
        ('Permissions',   {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'role', 'password1', 'password2'),
        }),
    )
