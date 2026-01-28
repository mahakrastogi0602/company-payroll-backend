# API Documentation - Django Employee Management System

## Base URL
```
http://localhost:8000/api/
```

## Authentication
Most endpoints are public except for salary increment which requires JWT authentication.

### Headers
```
Content-Type: application/json
Authorization: Bearer <access_token>  # For protected endpoints
```

---

## Table of Contents
1. [Employee Registration](#1-employee-registration)
2. [List All Employees](#2-list-all-employees)
3. [Get Specific Employee](#3-get-specific-employee)
4. [Get Top Employees](#4-get-top-employees)
5. [Increment Salary](#5-increment-salary)
6. [Get Statistics](#6-get-statistics)
7. [JWT Authentication](#7-jwt-authentication)

---

## 1. Employee Registration

Create a new employee with user account, contact information, and initial salary.

### Endpoint
```
POST /api/register/
```

### Authentication
Not required

### Request Body
```json
{
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
    "address": "123 Main St, New York, NY 10001",
    "phone": "+1234567890",
    "email": "john@example.com"
  },
  "salary": 50000
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | Unique username for login |
| email | string | Yes | User's email address |
| password | string | Yes | Password (will be hashed) |
| first_name | string | No | First name |
| last_name | string | No | Last name |
| city | string | No | City of residence |
| phone_number | string | No | Contact phone number |
| employee_code | string | Yes | Unique employee code |
| emp_num | string | Yes | Unique employee number |
| designation | string | Yes | Job title/position |
| contact | object | Yes | Contact information |
| contact.address | string | Yes | Physical address |
| contact.phone | string | Yes | Contact phone |
| contact.email | string | Yes | Contact email |
| salary | decimal | Yes | Initial salary amount |

### Success Response (201 Created)
```json
{
  "id": 1,
  "emp_num": "E001",
  "designation": "Software Engineer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "city": "New York",
    "phone_number": "+1234567890",
    "employee_code": "EMP001"
  },
  "contacts": [
    {
      "id": 1,
      "address": "123 Main St, New York, NY 10001",
      "phone": "+1234567890",
      "email": "john@example.com",
      "created_at": "2026-01-27T10:00:00Z",
      "updated_at": "2026-01-27T10:00:00Z"
    }
  ],
  "payrolls": [
    {
      "id": 1,
      "salary": "50000.00",
      "is_high_salary": true,
      "created_at": "2026-01-27T10:00:00Z",
      "updated_at": "2026-01-27T10:00:00Z"
    }
  ],
  "current_salary": "50000.00",
  "created_at": "2026-01-27T10:00:00Z",
  "updated_at": "2026-01-27T10:00:00Z"
}
```

### Error Response (400 Bad Request)
```json
{
  "employee_code": ["Employee code already exists."],
  "emp_num": ["Employee number already exists."],
  "username": ["Username already exists."]
}
```

### cURL Example
```bash
curl -X POST http://localhost:8000/api/register/ \
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
      "address": "123 Main St, New York, NY 10001",
      "phone": "+1234567890",
      "email": "john@example.com"
    },
    "salary": 50000
  }'
```

### Postman Setup
1. Method: POST
2. URL: `http://localhost:8000/api/register/`
3. Headers: `Content-Type: application/json`
4. Body: Raw JSON (see request body above)

---

## 2. List All Employees

Retrieve all employees with complete details including user info, contacts, and salary.

### Endpoint
```
GET /api/employees/
```

### Authentication
Not required

### Query Parameters
None

### Success Response (200 OK)
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "emp_num": "E001",
      "designation": "Software Engineer",
      "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "city": "New York",
        "phone_number": "+1234567890",
        "employee_code": "EMP001"
      },
      "contacts": [
        {
          "id": 1,
          "address": "123 Main St, New York, NY 10001",
          "phone": "+1234567890",
          "email": "john@example.com",
          "created_at": "2026-01-27T10:00:00Z",
          "updated_at": "2026-01-27T10:00:00Z"
        }
      ],
      "payrolls": [
        {
          "id": 1,
          "salary": "50000.00",
          "is_high_salary": true,
          "created_at": "2026-01-27T10:00:00Z",
          "updated_at": "2026-01-27T10:00:00Z"
        }
      ],
      "current_salary": "50000.00",
      "created_at": "2026-01-27T10:00:00Z",
      "updated_at": "2026-01-27T10:00:00Z"
    },
    {
      "id": 2,
      "emp_num": "E002",
      "designation": "Product Manager",
      "user": {
        "id": 2,
        "username": "jane_smith",
        "email": "jane@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "city": "Los Angeles",
        "phone_number": "+1987654321",
        "employee_code": "EMP002"
      },
      "contacts": [
        {
          "id": 2,
          "address": "456 Oak Ave, LA, CA 90001",
          "phone": "+1987654321",
          "email": "jane@example.com",
          "created_at": "2026-01-27T11:00:00Z",
          "updated_at": "2026-01-27T11:00:00Z"
        }
      ],
      "payrolls": [
        {
          "id": 2,
          "salary": "8000.00",
          "is_high_salary": false,
          "created_at": "2026-01-27T11:00:00Z",
          "updated_at": "2026-01-27T11:00:00Z"
        }
      ],
      "current_salary": "8000.00",
      "created_at": "2026-01-27T11:00:00Z",
      "updated_at": "2026-01-27T11:00:00Z"
    }
  ]
}
```

### cURL Example
```bash
curl http://localhost:8000/api/employees/
```

### Postman Setup
1. Method: GET
2. URL: `http://localhost:8000/api/employees/`

---

## 3. Get Specific Employee

Retrieve a specific employee by their employee number.

### Endpoint
```
GET /api/employee/<emp_num>/
```

### Authentication
Not required

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| emp_num | string | Employee number (e.g., "E001") |

### Success Response (200 OK)
```json
{
  "id": 1,
  "emp_num": "E001",
  "designation": "Software Engineer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "city": "New York",
    "phone_number": "+1234567890",
    "employee_code": "EMP001"
  },
  "contacts": [
    {
      "id": 1,
      "address": "123 Main St, New York, NY 10001",
      "phone": "+1234567890",
      "email": "john@example.com",
      "created_at": "2026-01-27T10:00:00Z",
      "updated_at": "2026-01-27T10:00:00Z"
    }
  ],
  "payrolls": [
    {
      "id": 1,
      "salary": "50000.00",
      "is_high_salary": true,
      "created_at": "2026-01-27T10:00:00Z",
      "updated_at": "2026-01-27T10:00:00Z"
    }
  ],
  "current_salary": "50000.00",
  "created_at": "2026-01-27T10:00:00Z",
  "updated_at": "2026-01-27T10:00:00Z"
}
```

### Error Response (404 Not Found)
```json
{
  "detail": "Not found."
}
```

### cURL Example
```bash
curl http://localhost:8000/api/employee/E001/
```

### Postman Setup
1. Method: GET
2. URL: `http://localhost:8000/api/employee/E001/`

---

## 4. Get Top Employees

Retrieve all employees with salary greater than 10,000.

### Endpoint
```
GET /api/top-employees/
```

### Authentication
Not required

### Filter Logic
Returns employees where the most recent payroll salary > 10,000

### Success Response (200 OK)
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "emp_num": "E001",
      "designation": "Software Engineer",
      "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "city": "New York",
        "phone_number": "+1234567890",
        "employee_code": "EMP001"
      },
      "contacts": [...],
      "payrolls": [
        {
          "id": 1,
          "salary": "50000.00",
          "is_high_salary": true,
          "created_at": "2026-01-27T10:00:00Z",
          "updated_at": "2026-01-27T10:00:00Z"
        }
      ],
      "current_salary": "50000.00",
      "created_at": "2026-01-27T10:00:00Z",
      "updated_at": "2026-01-27T10:00:00Z"
    }
  ]
}
```

### cURL Example
```bash
curl http://localhost:8000/api/top-employees/
```

### Postman Setup
1. Method: GET
2. URL: `http://localhost:8000/api/top-employees/`

---

## 5. Increment Salary

Increment employee salary based on current salary. **Requires JWT authentication.**

### Endpoint
```
POST /api/increment-salary/
```

### Authentication
**Required** - JWT Bearer Token

### Increment Logic

| Current Salary | Increment | New Salary |
|----------------|-----------|------------|
| < 10,000 | +2,000 | current + 2,000 |
| ≥ 10,000 | +5,000 | current + 5,000 |

### Request Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Request Body
```json
{
  "emp_num": "E001"
}
```

### Success Response (200 OK)
```json
{
  "id": 1,
  "emp_num": "E001",
  "designation": "Software Engineer",
  "user": {...},
  "contacts": [...],
  "payrolls": [
    {
      "id": 1,
      "salary": "50000.00",
      "is_high_salary": true,
      "created_at": "2026-01-27T10:00:00Z",
      "updated_at": "2026-01-27T10:00:00Z"
    },
    {
      "id": 2,
      "salary": "55000.00",
      "is_high_salary": true,
      "created_at": "2026-01-27T15:00:00Z",
      "updated_at": "2026-01-27T15:00:00Z"
    }
  ],
  "current_salary": "55000.00",
  "created_at": "2026-01-27T10:00:00Z",
  "updated_at": "2026-01-27T10:00:00Z"
}
```

### Error Responses

**401 Unauthorized** (No token provided):
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**400 Bad Request** (Invalid employee number):
```json
{
  "emp_num": ["Employee not found."]
}
```

### cURL Example
```bash
# First, get the token
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "SecurePass123!"}' \
  | jq -r '.access')

# Then use it to increment salary
curl -X POST http://localhost:8000/api/increment-salary/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"emp_num": "E001"}'
```

### Postman Setup
1. Method: POST
2. URL: `http://localhost:8000/api/increment-salary/`
3. Headers:
   - `Authorization: Bearer <access_token>`
   - `Content-Type: application/json`
4. Body: Raw JSON
   ```json
   {
     "emp_num": "E001"
   }
   ```

---

## 6. Get Statistics

Get overall statistics about employees and salaries.

### Endpoint
```
GET /api/stats/
```

### Authentication
Not required

### Success Response (200 OK)
```json
{
  "total_employees": 10,
  "high_salary_count": 5,
  "average_salary": 45000.00
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| total_employees | integer | Total number of employees |
| high_salary_count | integer | Number of employees with salary > 10,000 |
| average_salary | decimal | Average salary across all employees |

### cURL Example
```bash
curl http://localhost:8000/api/stats/
```

### Postman Setup
1. Method: GET
2. URL: `http://localhost:8000/api/stats/`

---

## 7. JWT Authentication

### 7.1 Obtain Token

Get JWT access and refresh tokens for authentication.

#### Endpoint
```
POST /api/token/
```

#### Request Body
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

#### Success Response (200 OK)
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Error Response (401 Unauthorized)
```json
{
  "detail": "No active account found with the given credentials"
}
```

#### cURL Example
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "SecurePass123!"}'
```

#### Token Lifetime
- **Access Token**: 1 hour
- **Refresh Token**: 1 day

---

### 7.2 Refresh Token

Get a new access token using the refresh token.

#### Endpoint
```
POST /api/token/refresh/
```

#### Request Body
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Success Response (200 OK)
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### cURL Example
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token_here"}'
```

---

## Complete API Flow Example

### Scenario: Register employee, list all, increment salary

```bash
# 1. Register a new employee
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_wonder",
    "email": "alice@example.com",
    "password": "SecurePass123!",
    "first_name": "Alice",
    "last_name": "Wonder",
    "city": "San Francisco",
    "phone_number": "+1555123456",
    "employee_code": "EMP003",
    "emp_num": "E003",
    "designation": "Data Scientist",
    "contact": {
      "address": "789 Pine St, SF, CA 94102",
      "phone": "+1555123456",
      "email": "alice@example.com"
    },
    "salary": 9000
  }'

# 2. List all employees
curl http://localhost:8000/api/employees/

# 3. Get specific employee
curl http://localhost:8000/api/employee/E003/

# 4. Get JWT token
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice_wonder", "password": "SecurePass123!"}' \
  | jq -r '.access')

# 5. Increment salary (9000 < 10000, so +2000 = 11000)
curl -X POST http://localhost:8000/api/increment-salary/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"emp_num": "E003"}'

# 6. Check top employees (should now include E003)
curl http://localhost:8000/api/top-employees/

# 7. Get statistics
curl http://localhost:8000/api/stats/
```

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required or failed |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Error Response Format
```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}
```

Or for general errors:
```json
{
  "detail": "Error message"
}
```

---

## Postman Collection

### Setting Up Environment Variables

1. Create a new environment in Postman
2. Add variables:
   - `base_url`: `http://localhost:8000/api`
   - `access_token`: (will be set automatically)
   - `refresh_token`: (will be set automatically)

### Pre-request Script for Token

Add this to requests that need authentication:

```javascript
// Get token if not exists or expired
if (!pm.environment.get("access_token")) {
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/token/",
        method: 'POST',
        header: {
            'Content-Type': 'application/json',
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                username: "your_username",
                password: "your_password"
            })
        }
    }, function (err, response) {
        const jsonResponse = response.json();
        pm.environment.set("access_token", jsonResponse.access);
        pm.environment.set("refresh_token", jsonResponse.refresh);
    });
}
```

---

## Rate Limiting & Best Practices

### Best Practices

1. **Always use HTTPS in production**
2. **Store tokens securely** (never in code or version control)
3. **Refresh tokens before expiry** (check token lifetime)
4. **Handle errors gracefully** (check status codes)
5. **Validate input data** (client-side validation)
6. **Use environment variables** (for different environments)

### Performance Tips

1. **Use pagination** for large datasets
2. **Cache responses** where appropriate
3. **Minimize nested data** if not needed
4. **Use database indexes** (already implemented)
5. **Monitor query performance** (Django Debug Toolbar)

---

## Support & Resources

- **Django REST Framework**: https://www.django-rest-framework.org/
- **JWT Documentation**: https://django-rest-framework-simplejwt.readthedocs.io/
- **Postman Documentation**: https://learning.postman.com/
