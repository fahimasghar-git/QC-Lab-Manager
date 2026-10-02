from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'department', 'is_approved', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('LIMS Info', {'fields': ('employee_id', 'department', 'is_approved', 'competence_summary')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('LIMS Info', {'fields': ('employee_id', 'department', 'is_approved', 'competence_summary')}),
    )

admin.site.register(User, CustomUserAdmin)
