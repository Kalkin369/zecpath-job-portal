 Authentication API Documentation

 Overview

This module handles user authentication using JWT (JSON Web Tokens).
It supports user registration, login, token refresh, and secure API access.

---

 1. Signup API

Endpoint

POST /api/auth/signup/

Request Body

{
  "email": "user@example.com",
  "password": "123456"
}

Response

{
  "message": "User created successfully"
}

---

 2. Login API

Endpoint

POST /api/auth/login/

Request Body

{
  "email": "user@example.com",
  "password": "123456"
}

Response

{
  "status": "success",
  "status_code": 200,
  "message": "Login successful",
  "data": {
    "access": "your_access_token",
    "refresh": "your_refresh_token"
  }
}

---

 3. Refresh Token API

Endpoint

POST /api/token/refresh/

Request Body

{
  "refresh": "your_refresh_token"
}

Response

{
  "access": "new_access_token"
}

---

 4. Authorization

All protected APIs require a Bearer Token.

Header Format

Authorization: Bearer <access_token>

---

 5. Authentication Flow

1. User registers using Signup API
2. User logs in → receives access & refresh token
3. Access token is used for API requests
4. If access token expires → use refresh token
5. New access token is generated

---

 Error Handling

Status Code| Meaning
400| Bad Request
401| Unauthorized
403| Forbidden
404| Not Found
500| Server Error

---

 Notes

- Access token expires in 15 minutes
- Refresh token expires in 1 day
- Tokens are stored in Postman environment variables
- All protected endpoints require authentication

---