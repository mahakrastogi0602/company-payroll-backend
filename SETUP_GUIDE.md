# Django Employee Management System - Setup Guide

## Step-by-Step Setup Instructions

This guide will walk you through setting up the Django Employee Management System from scratch.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: Check with `python3 --version`
- **MySQL 8.0+**: Check with `mysql --version`
- **pip**: Check with `pip3 --version`
- **Git** (optional): For version control

---

## Step 1: Set Up Python Environment

### 1.1 Navigate to Project Directory

```bash
cd /Users/mahak/Desktop/pro_active/Company
```

### 1.2 Create Virtual Environment

```bash
python3 -m venv venv
```

This creates an isolated Python environment for the project.

### 1.3 Activate Virtual Environment

**On macOS/Linux**:
```bash
source venv/bin/activate
```

**On Windows**:
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 1.4 Upgrade pip

```bash
pip install --upgrade pip
```

---

## Step 2: Install Dependencies

### 2.1 Install Python Packages

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2.9
- djangorestframework 3.14.0
- mysqlclient 2.2.1
- djangorestframework-simplejwt 5.3.1
- python-decouple 3.8

### 2.2 Verify Installation

```bash
pip list
```

You should see all the packages listed above.

---

## Step 3: Set Up MySQL Database

### 3.1 Start MySQL Service

**On macOS** (using Homebrew):
```bash
brew services start mysql
```

**On Ubuntu/Debian**:
```bash
sudo systemctl start mysql
```

**On Windows**:
- Start MySQL from Services or MySQL Workbench

### 3.2 Login to MySQL

```bash
mysql -u root -p
```

Enter your MySQL root password when prompted.

### 3.3 Create Database

```sql
CREATE DATABASE django_test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3.4 Verify Database Creation

```sql
SHOW DATABASES;
```

You should see `django_test_db` in the list.

### 3.5 Exit MySQL

```sql
EXIT;
```

---

## Step 4: Configure Environment Variables

### 4.1 Copy Environment Template

```bash
cp .env.example .env
```

### 4.2 Edit .env File

Open `.env` in your text editor and update:

```env
# Database Configuration
DB_NAME=django_test_db
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_HOST=localhost
DB_PORT=3306

# Django Settings
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Important**: Replace `your_mysql_password_here` with your actual MySQL password.

### 4.3 Generate Secret Key (Optional)

For a more secure secret key:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as your `SECRET_KEY` in `.env`.

---

## Step 5: Run Database Migrations

### 5.1 Create Migration Files

```bash
python manage.py makemigrations
```

Expected output:
```
Migrations for 'company_details':
  company_details/migrations/0001_initial.py
    - Create model CustomUser
    - Create model Employee
    - Create model Contact
    - Create model Payroll
```

### 5.2 Apply Migrations

```bash
python manage.py migrate
```

This creates all database tables.

### 5.3 Verify Migrations

```bash
python manage.py showmigrations
```

All migrations should have `[X]` marks.

---

## Step 6: Create Superuser

### 6.1 Run Createsuperuser Command

```bash
python manage.py createsuperuser
```

### 6.2 Enter Details

```
Username: admin
Email: admin@example.com
Password: ********
Password (again): ********
Employee code: ADMIN001
```

**Note**: You'll need to provide an employee code as it's a required field in the custom user model.

---

## Step 7: Run Development Server

### 7.1 Start Server

```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 7.2 Verify Server is Running

Open your browser and visit:
- **API Root**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## Step 8: Test the API

### 8.1 Test Employee Registration

Open a new terminal (keep the server running) and run:

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

### 8.2 Test List Employees

```bash
curl http://localhost:8000/api/employees/
```

### 8.3 Test Get Specific Employee

```bash
curl http://localhost:8000/api/employee/E001/
```

### 8.4 Test JWT Authentication

**Get Token**:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "SecurePass123!"}'
```

Save the `access` token from the response.

**Increment Salary** (replace `<TOKEN>` with your actual token):
```bash
curl -X POST http://localhost:8000/api/increment-salary/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"emp_num": "E001"}'
```

---

## Step 9: Access Admin Panel

### 9.1 Login to Admin

1. Visit http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Explore the admin interface

### 9.2 Admin Features

You can:
- View all users, employees, contacts, and payrolls
- Add, edit, and delete records
- Filter and search data
- View relationships between models

---

## Step 10: Using Postman (Optional)

### 10.1 Import Collection

1. Open Postman
2. Create a new collection: "Django Employee API"
3. Add requests for each endpoint

### 10.2 Set Up Environment

Create environment variables:
- `base_url`: `http://localhost:8000/api`
- `access_token`: (will be set after login)

### 10.3 Example Requests

**Register Employee**:
- Method: POST
- URL: `{{base_url}}/register/`
- Body: Raw JSON (see Step 8.1)

**Get Token**:
- Method: POST
- URL: `{{base_url}}/token/`
- Body: `{"username": "john_doe", "password": "SecurePass123!"}`

**Increment Salary**:
- Method: POST
- URL: `{{base_url}}/increment-salary/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body: `{"emp_num": "E001"}`

---

## Troubleshooting

### Issue 1: MySQL Connection Error

**Error**: `Can't connect to MySQL server`

**Solutions**:
1. Ensure MySQL is running:
   ```bash
   brew services list  # macOS
   sudo systemctl status mysql  # Linux
   ```

2. Check credentials in `.env` file

3. Test MySQL connection:
   ```bash
   mysql -u root -p -e "SELECT 1;"
   ```

### Issue 2: mysqlclient Installation Error

**Error**: `Failed building wheel for mysqlclient`

**Solutions**:

**On macOS**:
```bash
brew install mysql-client
export PATH="/usr/local/opt/mysql-client/bin:$PATH"
pip install mysqlclient
```

**On Ubuntu/Debian**:
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

### Issue 3: Migration Errors

**Error**: `No changes detected`

**Solution**:
```bash
python manage.py makemigrations company_details
python manage.py migrate
```

### Issue 4: Port Already in Use

**Error**: `Error: That port is already in use.`

**Solution**:
```bash
# Run on different port
python manage.py runserver 8001

# Or kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
```

### Issue 5: Permission Denied (MySQL)

**Error**: `Access denied for user 'root'@'localhost'`

**Solution**:
1. Reset MySQL password
2. Update `.env` file with correct password
3. Grant privileges:
   ```sql
   GRANT ALL PRIVILEGES ON django_test_db.* TO 'root'@'localhost';
   FLUSH PRIVILEGES;
   ```

---

## Next Steps

After successful setup:

1. **Read Documentation**:
   - [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
   - [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)

2. **Explore the Code**:
   - Review `models.py` for database structure
   - Check `serializers.py` for API logic
   - Examine `views.py` for endpoint implementation

3. **Test All Endpoints**:
   - Use the API documentation for examples
   - Test with different data
   - Verify error handling

4. **Customize**:
   - Add more fields to models
   - Create additional endpoints
   - Implement custom business logic

---

## Quick Reference

### Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

# Run shell
python manage.py shell

# Collect static files (production)
python manage.py collectstatic
```

### Database Commands

```bash
# MySQL login
mysql -u root -p

# Create database
mysql -u root -p -e "CREATE DATABASE django_test_db;"

# Backup database
mysqldump -u root -p django_test_db > backup.sql

# Restore database
mysql -u root -p django_test_db < backup.sql
```

---

## Support

If you encounter any issues not covered here:

1. Check the error message carefully
2. Review the documentation files
3. Search Django documentation
4. Check Django REST Framework docs

---

**Setup Complete! 🎉**

You now have a fully functional Django Employee Management System with REST API, JWT authentication, and comprehensive documentation.
