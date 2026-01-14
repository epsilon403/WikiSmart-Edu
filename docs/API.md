# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Authentication Endpoints

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "role": "user"
}
```

#### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "role": "string"
  }
}
```

### Content Endpoints

#### Summarize Article
```http
POST /content/summarize
```

**Request Body:**
```json
{
  "url": "https://en.wikipedia.org/wiki/...",
  "summary_type": "short|medium"
}
```

**Response:**
```json
{
  "article_id": "integer",
  "title": "string",
  "summary": "string",
  "created_at": "datetime"
}
```

#### Translate Content
```http
POST /content/translate
```

**Request Body:**
```json
{
  "article_id": "integer",
  "target_language": "fr|en|ar|es"
}
```

**Response:**
```json
{
  "original_text": "string",
  "translated_text": "string",
  "target_language": "string"
}
```

#### Export as PDF
```http
POST /content/export/pdf
```

**Request Body:**
```json
{
  "article_id": "integer",
  "content_type": "summary|translation|quiz"
}
```

**Response:**
Binary PDF file

#### Export as TXT
```http
POST /content/export/txt
```

**Request Body:**
```json
{
  "article_id": "integer",
  "content_type": "summary|translation|quiz"
}
```

**Response:**
Binary TXT file

### Quiz Endpoints

#### Generate Quiz
```http
POST /quiz/generate
```

**Request Body:**
```json
{
  "article_id": "integer",
  "num_mcq": "integer",
  "num_open": "integer"
}
```

**Response:**
```json
{
  "quiz_id": "integer",
  "questions": [
    {
      "id": "integer",
      "type": "mcq|open",
      "question": "string",
      "options": ["string"],  // Only for MCQ
      "correct_answer": "string"
    }
  ]
}
```

#### Submit Quiz
```http
POST /quiz/submit
```

**Request Body:**
```json
{
  "quiz_id": "integer",
  "answers": [
    {
      "question_id": "integer",
      "answer": "string"
    }
  ]
}
```

**Response:**
```json
{
  "attempt_id": "integer",
  "score": "float",
  "total_questions": "integer",
  "correct_answers": "integer",
  "feedback": [
    {
      "question_id": "integer",
      "is_correct": "boolean",
      "user_answer": "string",
      "correct_answer": "string"
    }
  ]
}
```

#### Get Quiz Results
```http
GET /quiz/results/{attempt_id}
```

**Response:**
```json
{
  "attempt_id": "integer",
  "score": "float",
  "submitted_at": "datetime",
  "article": {
    "id": "integer",
    "title": "string"
  }
}
```

### User Endpoints

#### Get Profile
```http
GET /users/profile
```

**Response:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "role": "string",
  "created_at": "datetime"
}
```

#### Get History
```http
GET /users/history
```

**Response:**
```json
{
  "articles": [
    {
      "id": "integer",
      "title": "string",
      "url": "string",
      "action": "summarize|translate|quiz",
      "created_at": "datetime"
    }
  ],
  "quiz_attempts": [
    {
      "id": "integer",
      "article_title": "string",
      "score": "float",
      "submitted_at": "datetime"
    }
  ]
}
```

### Admin Endpoints

#### Get Statistics
```http
GET /admin/statistics
```

**Response:**
```json
{
  "total_users": "integer",
  "total_articles": "integer",
  "total_quizzes": "integer",
  "total_downloads": "integer",
  "registrations_by_month": [
    {
      "month": "string",
      "count": "integer"
    }
  ]
}
```

#### Get All Users
```http
GET /admin/users
```

**Response:**
```json
{
  "users": [
    {
      "id": "integer",
      "username": "string",
      "email": "string",
      "role": "string",
      "created_at": "datetime"
    }
  ]
}
```

#### Delete User
```http
DELETE /admin/users/{user_id}
```

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse. Current limits:
- 100 requests per minute per user
- 1000 requests per hour per user

## Pagination

List endpoints support pagination using query parameters:
```
?page=1&limit=10
```

Default limit: 10
Maximum limit: 100
