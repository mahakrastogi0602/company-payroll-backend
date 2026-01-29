# Django Employee Management System

A Django REST API for managing employees, contacts, and payroll with JWT authentication.

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: MySQL 8.0
- **Authentication**: JWT (SimpleJWT)
- **Containerization**: Docker Compose

## Features

- Custom User Model with employee-specific fields
- Employee registration with contact and payroll information
- JWT-based authentication for protected endpoints
- Salary increment with business logic
- Query optimization using select_related/prefetch_related

## Project Structure

```
Company/
├── Company/                 # Project configuration
│   ├── settings.py
│   └── urls.py
├── company_details/         # Main application
│   ├── models.py           # CustomUser, Employee, Contact, Payroll
│   ├── serializers.py      # Data validation & transformation
│   ├── views.py            # API endpoints
│   └── urls.py             # URL routing
├── docker-compose.yml       # MySQL container
└── requirements.txt
```

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/mahakrastogi0602/company-payroll-backend.git
cd company-payroll-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start MySQL with Docker

```bash
docker compose up -d
```

This starts MySQL 8.0 on port 3306 with:
- Database: `django_test_db`
- User: `root`
- Password: `root_password`

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env if you need different database credentials
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

Server runs at: http://127.0.0.1:8000

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Get JWT access & refresh tokens |
| POST | `/api/token/refresh/` | Refresh access token |

### Employee Management

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/register/` | Register new employee | ❌ |
| GET | `/api/employees/` | List all employees | ❌ |
| GET | `/api/employee/<emp_num>/` | Get employee details | ❌ |
| GET | `/api/top-employees/` | Employees with salary > 10,000 | ❌ |
| POST | `/api/increment-salary/` | Increment employee salary | ✅ |

## API Examples

### Register Employee

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "city": "New York",
    "phone_number": "+1234567890",
    "employee_code": "EMP001",
    "emp_num": "E001",
    "designation": "Software Engineer",
    "contact": {
      "address": "123 Main St, NY",
      "phone": "+1234567890",
      "email": "john@example.com"
    },
    "salary": 50000
  }'
```

### Get JWT Token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "SecurePass123!"}'
```

### Increment Salary (Protected)

```bash
curl -X POST http://127.0.0.1:8000/api/increment-salary/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"emp_num": "E001"}'
```

## Database Schema

```
CustomUser (1) ──── (1) Employee (1) ──── (N) Contact
                          │
                          └──── (N) Payroll
```

## Salary Increment Logic

- If current salary < 10,000: increment by 2,000
- If current salary ≥ 10,000: increment by 5,000

Each increment creates a new Payroll record, maintaining salary history.

## License

This project is for educational purposes.
