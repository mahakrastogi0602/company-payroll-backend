from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Employee, Payroll
from .serializers import (
    EmployeeSerializer,
    EmployeeRegistrationSerializer,
    SalaryIncrementSerializer
)


class RegisterEmployeeView(APIView):
    """
    POST /api/register/
    
    Register a new employee with user account, contact, and payroll information.
    Creates User, Employee, Contact, and Payroll in a single transaction.
    
    Request Body:
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
    
    Response: Complete employee data with nested user, contact, and payroll
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = EmployeeRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                serializer.to_representation(employee),
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class EmployeeListView(APIView):
    """
    GET /api/employees/
    
    Get all employees with complete details including:
    - Employee number and designation
    - User information (username, email, city, phone)
    - Contact details
    - Salary information
    
    Response: List of all employees with nested data
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        employees = Employee.objects.all().select_related('user').prefetch_related(
            'contacts', 'payrolls'
        )
        serializer = EmployeeSerializer(employees, many=True)
        
        return Response({
            'count': employees.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)


class EmployeeDetailView(APIView):
    """
    GET /api/employee/<emp_num>/
    
    Get specific employee details by employee number.
    
    Path Parameter:
    - emp_num: Employee number (e.g., "E001")
    
    Response: Complete employee data with nested information
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request, emp_num):
        employee = get_object_or_404(
            Employee.objects.select_related('user').prefetch_related(
                'contacts', 'payrolls'
            ),
            emp_num=emp_num
        )
        serializer = EmployeeSerializer(employee)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TopEmployeesView(APIView):
    """
    GET /api/top-employees/
    
    Get all employees with salary greater than 10,000.
    Filters based on the most recent payroll record for each employee.
    
    Response: List of high-salary employees with complete details
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Get all employees
        all_employees = Employee.objects.all().select_related('user').prefetch_related(
            'contacts', 'payrolls'
        )
        
        # Filter employees with salary > 10000
        high_salary_employees = []
        for employee in all_employees:
            latest_payroll = employee.payrolls.order_by('-created_at').first()
            if latest_payroll and latest_payroll.salary > 10000:
                high_salary_employees.append(employee)
        
        serializer = EmployeeSerializer(high_salary_employees, many=True)
        
        return Response({
            'count': len(high_salary_employees),
            'results': serializer.data
        }, status=status.HTTP_200_OK)


class IncrementSalaryView(APIView):
    """
    POST /api/increment-salary/
    
    Increment employee salary based on current salary:
    - If salary < 10,000: add 2,000
    - If salary >= 10,000: add 5,000
    
    Creates a new payroll record to maintain salary history.
    Requires JWT authentication.
    
    Request Body:
    {
        "emp_num": "E001"
    }
    
    Response: Updated employee data with new salary
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = SalaryIncrementSerializer(data=request.data)
        
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                serializer.to_representation(employee),
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class EmployeeStatsView(APIView):
    """
    GET /api/stats/
    
    Get statistics about employees and salaries.
    
    Response:
    {
        "total_employees": 10,
        "high_salary_count": 5,
        "average_salary": 45000.00
    }
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        from django.db.models import Avg
        
        total_employees = Employee.objects.count()
        
        # Count high salary employees
        all_employees = Employee.objects.all().prefetch_related('payrolls')
        high_salary_count = 0
        total_salary = 0
        
        for employee in all_employees:
            latest_payroll = employee.payrolls.order_by('-created_at').first()
            if latest_payroll:
                if latest_payroll.salary > 10000:
                    high_salary_count += 1
                total_salary += float(latest_payroll.salary)
        
        average_salary = total_salary / total_employees if total_employees > 0 else 0
        
        return Response({
            'total_employees': total_employees,
            'high_salary_count': high_salary_count,
            'average_salary': round(average_salary, 2)
        }, status=status.HTTP_200_OK)
