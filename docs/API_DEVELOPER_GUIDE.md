# Zecpath Recruitment Platform
## Developer Integration Guide

Version: 1.0.0

---

# 1. Project Overview

Zecpath is an AI-powered Recruitment Platform built with:

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- AWS S3
- OpenAI
- ElevenLabs
- Twilio
- Razorpay

The platform supports:

- Candidate Management
- Employer Management
- Job Posting
- Application Tracking
- Interview Scheduling
- AI Interviews
- Candidate Evaluation
- Reporting
- Subscription Billing

---

# 2. Installation

## Clone Repository

git clone <repository_url>

cd zecpath_backend

---

## Create Virtual Environment

python -m venv env

### Windows

env\Scripts\activate

### Linux

source env/bin/activate

---

## Install Dependencies

pip install -r requirements.txt

---

# 3. Environment Variables

Create:

.env

Example:

SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=zecpath
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=app-password

OPENAI_API_KEY=xxxxxxxx

ELEVENLABS_API_KEY=xxxxxxxx

TWILIO_API_KEY=xxxxxxxx

RAZORPAY_KEY_ID=xxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxx
RAZORPAY_WEBHOOK_SECRET=xxxxxxxx

AWS_ACCESS_KEY_ID=xxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxx
AWS_STORAGE_BUCKET_NAME=xxxxxxxx
AWS_S3_REGION_NAME=xxxxxxxx

AWS_CLOUDFRONT_DOMAIN=xxxxxxxx

---

# 4. Database Setup

Run migrations:

python manage.py migrate

Create admin user:

python manage.py createsuperuser

---

# 5. Running the Project

Run server:

python manage.py runserver

Default:

http://127.0.0.1:8000/

---

# 6. API Documentation

Swagger UI:

http://127.0.0.1:8000/api/docs/

ReDoc:

http://127.0.0.1:8000/api/redoc/

OpenAPI Schema:

http://127.0.0.1:8000/api/schema/

---

# 7. Authentication

Zecpath uses JWT Authentication.

## Login

POST

/api/auth/login/

Request

{
    "email": "user@example.com",
    "password": "password"
}

Response

{
    "access": "...",
    "refresh": "..."
}

---

# 8. Swagger Authentication

Click:

Authorize

Enter:

Bearer <access_token>

Example:

Bearer eyJhbGciOiJIUzI1Ni...

Click:

Authorize

All protected APIs are now accessible.

---

# 9. API Modules

Authentication

- Signup
- Login
- Logout
- Refresh Token

Candidate

- Candidate CRUD
- Resume Upload
- Saved Jobs

Employer

- Employer CRUD
- Employer Verification

Jobs

- Job CRUD
- Job Search
- Job Filtering

Applications

- Apply Job
- Application Tracking

Interview

- Schedule Interview
- Reschedule Interview
- Interview Availability

AI

- Generate Questions
- Text To Speech
- Speech To Text
- Voice Call
- Answer Evaluation

Finance

- Dashboard
- Revenue Analytics
- Payment Failures

Admin

- User Management
- Employer Approval
- Spam Job Removal
- Platform Statistics

---

# 10. Common Error Responses

400 Bad Request

{
    "error": "Invalid request"
}

401 Unauthorized

{
    "detail": "Authentication credentials were not provided."
}

403 Forbidden

{
    "detail": "Permission denied."
}

404 Not Found

{
    "error": "Resource not found"
}

500 Internal Server Error

{
    "error": "Unexpected server error"
}

---

# 11. Rate Limiting

Interview APIs

20 requests/minute

Login APIs

5 requests/minute

Premium Recruiter APIs

20 requests/hour

---

# 12. Background Services

Redis

Used for:

- Cache
- Celery Queue

Start Redis:

redis-server

---

Celery Worker

celery -A zecpath_backend worker -l info

---

# 13. File Storage

AWS S3 is used for:

- Resume Storage
- Candidate Documents

CloudFront is used for file delivery.

---

# 14. Deployment Checklist

Production Settings

DEBUG=False

Configure:

ALLOWED_HOSTS

Setup:

- PostgreSQL
- Redis
- Celery
- AWS S3

Collect Static Files

python manage.py collectstatic

Run Migrations

python manage.py migrate

---

# 15. Testing

Generate Schema

python manage.py spectacular --file schema.yml

Run Tests

python manage.py test

API Testing

Swagger UI
Postman

---

# 16. Maintainers

Zecpath Backend Team

Version: 1.0.0