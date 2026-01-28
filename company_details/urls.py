from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterEmployeeView,
    EmployeeListView,
    EmployeeDetailView,
    TopEmployeesView,
    IncrementSalaryView,
    EmployeeStatsView
)

urlpatterns = [
    # Employee Management APIs
    path('register/', RegisterEmployeeView.as_view(), name='register-employee'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/<str:emp_num>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('top-employees/', TopEmployeesView.as_view(), name='top-employees'),
    path('increment-salary/', IncrementSalaryView.as_view(), name='increment-salary'),
    path('stats/', EmployeeStatsView.as_view(), name='employee-stats'),
    
    # JWT Authentication APIs
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
