from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Skill

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'user_type', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active', 'status', 'date_joined')
    search_fields = ('email', 'full_name', 'company_name')
    ordering = ('email',)
    filter_horizontal = ('skills', 'groups', 'user_permissions')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'profile_picture')}),
        ('User Type & Status', {'fields': ('user_type', 'status')}),
        ('Student Fields', {
            'fields': ('education', 'skills', 'resume'),
            'classes': ('collapse',),
        }),
        ('Employer Fields', {
            'fields': ('company_name', 'company_website', 'company_description'),
            'classes': ('collapse',),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'user_type', 'password1', 'password2'),
        }),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
