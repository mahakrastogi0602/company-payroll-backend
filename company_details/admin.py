from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Employee, Contact, Payroll


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    Extends Django's UserAdmin to include custom fields.
    """
    
    list_display = [
        'username', 'email', 'employee_code',
        'city', 'phone_number', 'is_staff', 'is_active'
    ]
    
    list_filter = [
        'is_staff', 'is_active', 'city', 'date_joined'
    ]
    
    search_fields = [
        'username', 'email', 'employee_code',
        'first_name', 'last_name', 'city'
    ]
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('city', 'phone_number', 'employee_code')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('city', 'phone_number', 'employee_code')
        }),
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Admin interface for Employee model.
    """
    
    list_display = [
        'emp_num', 'designation', 'user',
        'current_salary', 'created_at'
    ]
    
    list_filter = [
        'designation', 'created_at'
    ]
    
    search_fields = [
        'emp_num', 'designation',
        'user__username', 'user__email', 'user__employee_code'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('emp_num', 'designation', 'user')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin interface for Contact model.
    """
    
    list_display = [
        'employee', 'email', 'phone', 'created_at'
    ]
    
    list_filter = [
        'created_at'
    ]
    
    search_fields = [
        'email', 'phone', 'address',
        'employee__emp_num', 'employee__user__username'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('employee', 'address', 'phone', 'email')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    """
    Admin interface for Payroll model.
    """
    
    list_display = [
        'employee', 'salary', 'is_high_salary', 'created_at'
    ]
    
    list_filter = [
        'created_at', 'salary'
    ]
    
    search_fields = [
        'employee__emp_num', 'employee__user__username'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Payroll Information', {
            'fields': ('employee', 'salary')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_high_salary(self, obj):
        """Display if salary is high (>10000)."""
        return obj.is_high_salary
    
    is_high_salary.boolean = True
    is_high_salary.short_description = 'High Salary'
