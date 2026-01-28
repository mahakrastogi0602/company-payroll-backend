from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db import transaction
from .models import CustomUser, Employee, Contact, Payroll


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    Handles user creation with password hashing.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'password',
            'first_name', 'last_name', 'city',
            'phone_number', 'employee_code'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model.
    """
    class Meta:
        model = Contact
        fields = ['id', 'address', 'phone', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PayrollSerializer(serializers.ModelSerializer):
    """
    Serializer for Payroll model.
    """
    is_high_salary = serializers.ReadOnlyField()
    
    class Meta:
        model = Payroll
        fields = ['id', 'salary', 'is_high_salary', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model with nested relationships.
    Includes user details, contacts, and payroll information.
    """
    user = CustomUserSerializer(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    payrolls = PayrollSerializer(many=True, read_only=True)
    current_salary = serializers.ReadOnlyField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'emp_num', 'designation', 'user',
            'contacts', 'payrolls', 'current_salary',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeRegistrationSerializer(serializers.Serializer):
    """
    Serializer for employee registration.
    Handles creation of User, Employee, Contact, and Payroll in a single transaction.
    
    Request Format:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "secure_password",
        "first_name": "John",
        "last_name": "Doe",
        "city": "New York",
        "phone_number": "+1234567890",
        "employee_code": "EMP001",
        "emp_num": "E001",
        "designation": "Software Engineer",
        "contact": {
            "address": "123 Main St, New York, NY",
            "phone": "+1234567890",
            "email": "john@example.com"
        },
        "salary": 50000
    }
    """
    
    # User fields
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    employee_code = serializers.CharField(max_length=20)
    
    # Employee fields
    emp_num = serializers.CharField(max_length=20)
    designation = serializers.CharField(max_length=100)
    
    # Contact fields (nested)
    contact = ContactSerializer()
    
    # Payroll fields
    salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_employee_code(self, value):
        """Check if employee code already exists."""
        if CustomUser.objects.filter(employee_code=value).exists():
            raise serializers.ValidationError("Employee code already exists.")
        return value
    
    def validate_emp_num(self, value):
        """Check if employee number already exists."""
        if Employee.objects.filter(emp_num=value).exists():
            raise serializers.ValidationError("Employee number already exists.")
        return value
    
    def validate_username(self, value):
        """Check if username already exists."""
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Create User, Employee, Contact, and Payroll in a single transaction.
        If any step fails, all changes are rolled back.
        """
        # Extract nested contact data
        contact_data = validated_data.pop('contact')
        
        # Extract employee-specific data
        emp_num = validated_data.pop('emp_num')
        designation = validated_data.pop('designation')
        salary = validated_data.pop('salary')
        
        # Create CustomUser
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            city=validated_data.get('city', ''),
            phone_number=validated_data.get('phone_number', ''),
            employee_code=validated_data['employee_code']
        )
        
        # Create Employee
        employee = Employee.objects.create(
            emp_num=emp_num,
            designation=designation,
            user=user
        )
        
        # Create Contact
        contact = Contact.objects.create(
            employee=employee,
            **contact_data
        )
        
        # Create Payroll
        payroll = Payroll.objects.create(
            employee=employee,
            salary=salary
        )
        
        return employee
    
    def to_representation(self, instance):
        """Return the created employee with all nested data."""
        return EmployeeSerializer(instance).data


class SalaryIncrementSerializer(serializers.Serializer):
    """
    Serializer for salary increment operation.
    
    Request Format:
    {
        "emp_num": "E001"
    }
    
    Logic:
    - If current salary < 10000: add 2000
    - If current salary >= 10000: add 5000
    """
    
    emp_num = serializers.CharField(max_length=20)
    
    def validate_emp_num(self, value):
        """Check if employee exists."""
        try:
            Employee.objects.get(emp_num=value)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Employee not found.")
        return value
    
    @transaction.atomic
    def save(self):
        """
        Increment salary based on current salary and create new payroll record.
        """
        emp_num = self.validated_data['emp_num']
        employee = Employee.objects.get(emp_num=emp_num)
        
        # Get current salary
        current_payroll = employee.payrolls.order_by('-created_at').first()
        current_salary = current_payroll.salary if current_payroll else 0
        
        # Calculate increment
        if current_salary < 10000:
            new_salary = current_salary + 2000
        else:
            new_salary = current_salary + 5000
        
        # Create new payroll record
        new_payroll = Payroll.objects.create(
            employee=employee,
            salary=new_salary
        )
        
        return employee
    
    def to_representation(self, instance):
        """Return the updated employee with new salary."""
        return EmployeeSerializer(instance).data
