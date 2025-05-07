# Coreuser/admin.py
from django.contrib import admin
from .models import Coreuser

@admin.register(Coreuser)
class CoreuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phone', 'department', 'is_super_admin', 'is_staff')
    search_fields = ('username', 'name', 'email', 'phone')
    list_filter = ('department', 'is_super_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('name', 'email', 'phone', 'department')}),
        ('权限信息', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_super_admin', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('个人信息', {'fields': ('name', 'email', 'phone', 'department')}),
        ('权限信息', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_super_admin', 'groups', 'user_permissions')}),
    )
    ordering = ('-date_joined',)