from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser.
    
    Additional Fields:
    - city: User's city of residence
    - phone_number: Contact phone number
    - employee_code: Unique employee identifier
    
    Inherits from AbstractUser:
    - username, email, password, first_name, last_name, is_staff, is_active, date_joined
    """
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City of residence"
    )
    
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )
    
    employee_code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique employee code"
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.employee_code})"


class Employee(models.Model):
    """
    Employee Model with OneToOne relationship to CustomUser.
    
    Fields:
    - emp_num: Unique employee number
    - designation: Job title/position
    - user: OneToOne link to CustomUser
    """
    
    emp_num = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique employee number"
    )
    
    designation = models.CharField(
        max_length=100,
        help_text="Job title or position"
    )
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee',
        help_text="Associated user account"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ['emp_num']
    
    def __str__(self):
        return f"{self.emp_num} - {self.user.username} ({self.designation})"
    
    @property
    def current_salary(self):
        """Get the most recent salary for this employee."""
        latest_payroll = self.payrolls.order_by('-created_at').first()
        return latest_payroll.salary if latest_payroll else 0


class Contact(models.Model):
    """
    Contact Model with ForeignKey relationship to Employee.
    Multiple contacts can be associated with one employee.
    
    Fields:
    - address: Physical address
    - phone: Contact phone number
    - email: Contact email address
    - employee: ForeignKey to Employee
    """
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    address = models.TextField(
        help_text="Physical address"
    )
    
    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        help_text="Contact phone number"
    )
    
    email = models.EmailField(
        help_text="Contact email address"
    )
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='contacts',
        help_text="Associated employee"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact for {self.employee.emp_num} - {self.email}"


class Payroll(models.Model):
    """
    Payroll Model with ForeignKey relationship to Employee.
    Maintains salary history for each employee.
    
    Fields:
    - salary: Employee salary amount
    - employee: ForeignKey to Employee
    - created_at: When this payroll record was created
    - updated_at: When this payroll record was last updated
    """
    
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Employee salary"
    )
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='payrolls',
        help_text="Associated employee"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Payroll record creation date"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Payroll record last update date"
    )
    
    class Meta:
        verbose_name = "Payroll"
        verbose_name_plural = "Payrolls"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['employee', '-created_at']),
        ]
    
    def __str__(self):
        return f"Payroll for {self.employee.emp_num} - ${self.salary}"
    
    @property
    def is_high_salary(self):
        """Check if salary is above 10000."""
        return self.salary > 10000
