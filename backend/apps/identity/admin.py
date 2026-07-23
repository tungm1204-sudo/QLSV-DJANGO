from django.contrib import admin

from .models import User, Role, OTPToken, LoginSession

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'status', 'role', 'created_at')
    search_fields = ('email', 'full_name')
    list_filter = ('status', 'role')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(OTPToken)
class OTPTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'type', 'expires_at', 'is_used')
    list_filter = ('type', 'is_used')
    search_fields = ('user__email', 'code')

@admin.register(LoginSession)
class LoginSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'ip_address')
