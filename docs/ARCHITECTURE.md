# WikiSmart-Edu Architecture

## System Overview

WikiSmart-Edu is a full-stack educational platform built with a modern microservices-inspired architecture. The system consists of three main layers:

1. **Frontend Layer**: React.js SPA or Streamlit application
2. **Backend Layer**: FastAPI REST API
3. **Data Layer**: PostgreSQL database

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                        │
│  ┌─────────────────────┐    ┌─────────────────────┐    │
│  │   React.js SPA      │    │  Streamlit App      │    │
│  │  - Components       │    │  - Pages            │    │
│  │  - Services         │    │  - Components       │    │
│  │  - State Management │    │  - API Client       │    │
│  └──────────┬──────────┘    └──────────┬──────────┘    │
└─────────────┼──────────────────────────┼────────────────┘
              │                          │
              └──────────┬───────────────┘
                         │ HTTP/REST
              ┌──────────▼──────────┐
              │   API Gateway       │
              │  (FastAPI Router)   │
              └──────────┬──────────┘
                         │
┌─────────────────────────┼────────────────────────────────┐
│                Backend Layer                              │
│  ┌──────────────────────▼─────────────────────────────┐ │
│  │              API Routes                             │ │
│  │  /auth  /users  /articles  /quiz  /admin          │ │
│  └──────────┬─────────────────────────────────────────┘ │
│             │                                            │
│  ┌──────────▼─────────────────────────────────────────┐ │
│  │           Business Logic Layer                      │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │ │
│  │  │   Content   │  │     LLM     │  │    Auth    │ │ │
│  │  │  Extractor  │  │   Services  │  │  Service   │ │ │
│  │  └─────────────┘  └─────────────┘  └────────────┘ │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │ │
│  │  │Preprocessor │  │   Export    │  │Validators  │ │ │
│  │  └─────────────┘  └─────────────┘  └────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
│                         │                                │
│  ┌──────────────────────▼───────────────────────────┐  │
│  │              Data Access Layer                    │  │
│  │                (SQLAlchemy ORM)                   │  │
│  └──────────────────────┬───────────────────────────┘  │
└─────────────────────────┼──────────────────────────────┘
                          │
              ┌───────────▼──────────┐
              │  PostgreSQL Database │
              │  - users             │
              │  - articles          │
              │  - quiz_attempts     │
              └──────────────────────┘

External Services:
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Groq API     │    │ Gemini API   │    │ Wikipedia    │
│ (Summary)    │    │(Translation, │    │    API       │
│              │    │    Quiz)     │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Component Details

### 1. Frontend Layer

#### React Application
- **Structure**: Component-based architecture
- **State Management**: React Context API + hooks
- **Routing**: React Router v6
- **UI Framework**: Material-UI (MUI)
- **HTTP Client**: Axios

**Key Components:**
- `Auth/`: Login and registration
- `Article/`: Article input, display, history
- `Quiz/`: Quiz display, questions, results
- `Admin/`: Dashboard, user management, statistics
- `Common/`: Reusable UI components

#### Streamlit Application
- **Structure**: Page-based multi-page app
- **State Management**: Streamlit session state
- **HTTP Client**: Requests library

**Pages:**
- Articles processing
- Quiz generation and taking
- History and progress tracking
- Admin dashboard

### 2. Backend Layer

#### API Layer (`app/api/`)
- RESTful API endpoints
- Request validation with Pydantic
- Dependency injection for auth and database
- API versioning (`/api/v1/`)

**Route Groups:**
- `auth.py`: Authentication and authorization
- `users.py`: User profile and history
- `articles.py`: Article management
- `quiz.py`: Quiz generation and submission
- `content.py`: Content processing (summary, translation, export)
- `admin.py`: Admin operations and statistics

#### Service Layer (`app/services/`)

**Content Services:**
- `content_extractor.py`: Extract text from Wikipedia URLs and PDFs
- `preprocessor.py`: Parse URLs, segment articles into sections
- `export_service.py`: Generate PDF and TXT exports

**LLM Services:**
- `llm_service.py`: Base LLM service interface
- `groq_service.py`: Groq integration for summarization
- `gemini_service.py`: Gemini integration for translation and quiz generation

**Other Services:**
- `auth_service.py`: OAuth 2.0 + JWT authentication

#### Core Layer (`app/core/`)
- `security.py`: Password hashing, JWT token management
- `config.py`: Application configuration with pydantic-settings
- `exceptions.py`: Custom exceptions and error handling

#### Middleware (`app/middleware/`)
- `error_handler.py`: Global exception handling
- `logging.py`: Structured logging

#### Models (`app/models/`)
SQLAlchemy ORM models:
- `user.py`: User account and authentication
- `article.py`: Processed articles
- `quiz_attempt.py`: Quiz submissions and scores

#### Schemas (`app/schemas/`)
Pydantic validation schemas for:
- Request validation
- Response serialization
- Data transfer objects (DTOs)

### 3. Data Layer

#### Database Schema

**users**
```sql
id: INTEGER PRIMARY KEY
username: VARCHAR(50) UNIQUE NOT NULL
email: VARCHAR(100) UNIQUE NOT NULL
hashed_password: VARCHAR(255) NOT NULL
role: VARCHAR(20) DEFAULT 'user'
created_at: TIMESTAMP DEFAULT NOW()
```

**articles**
```sql
id: INTEGER PRIMARY KEY
user_id: INTEGER REFERENCES users(id)
url: VARCHAR(500)
title: VARCHAR(255)
action: VARCHAR(50)  -- 'summarize', 'translate', 'quiz'
created_at: TIMESTAMP DEFAULT NOW()
```

**quiz_attempts**
```sql
id: INTEGER PRIMARY KEY
user_id: INTEGER REFERENCES users(id)
article_id: INTEGER REFERENCES articles(id)
score: FLOAT
submitted_at: TIMESTAMP DEFAULT NOW()
```

## Data Flow

### 1. Article Summarization Flow

```
User → Frontend → POST /api/v1/content/summarize
                 ↓
         FastAPI Route Handler
                 ↓
         Validate Request (Pydantic)
                 ↓
         Content Extractor Service
                 ↓
    Extract from Wikipedia/PDF
                 ↓
         Preprocessor Service
                 ↓
    Parse URL, Segment Sections
                 ↓
         Groq Service
                 ↓
    Generate Summary with LLM
                 ↓
         Save to Database
                 ↓
         Return Response → Frontend
```

### 2. Quiz Generation Flow

```
User → Frontend → POST /api/v1/quiz/generate
                 ↓
         FastAPI Route Handler
                 ↓
         Get Article Content
                 ↓
         Gemini Service
                 ↓
    Generate Quiz (MCQ + Open Questions)
                 ↓
         Parse JSON Response
                 ↓
         Save Quiz Data
                 ↓
         Return Questions → Frontend
```

### 3. Authentication Flow

```
User → Frontend → POST /api/v1/auth/login
                 ↓
         Auth Route
                 ↓
         Verify Credentials
                 ↓
         Generate JWT Token
                 ↓
         Return Token → Frontend
                 ↓
    Store in localStorage/Cookie
                 ↓
    Include in Authorization Header
    for Protected Requests
```

## Security Architecture

### Authentication & Authorization
- **JWT Tokens**: Stateless authentication
- **OAuth 2.0**: Industry-standard protocol
- **Password Hashing**: bcrypt for secure storage
- **Role-Based Access**: User and admin roles

### API Security
- **CORS**: Configurable allowed origins
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM

## Scalability Considerations

### Horizontal Scaling
- Stateless backend allows multiple instances
- Load balancer in front of API servers
- Database connection pooling

### Caching Strategy
- Redis for session storage (future)
- LLM response caching
- Static asset CDN

### Performance Optimization
- Async/await for I/O operations
- Database query optimization
- Lazy loading for relationships

## Testing Strategy

### Backend Testing
- **Unit Tests**: Test individual functions and services
- **Integration Tests**: Test API endpoints
- **Mocking**: Mock external LLM APIs

### Frontend Testing
- **Component Tests**: Test React components
- **Integration Tests**: Test user flows
- **E2E Tests**: Cypress/Playwright (future)

## Deployment Architecture

### Development
```
Local Machine
├── Backend (uvicorn)
├── Frontend (npm start / streamlit)
└── PostgreSQL (local/Docker)
```

### Production (Docker Compose)
```
Docker Host
├── Nginx (Reverse Proxy)
├── Backend Container (FastAPI)
├── Frontend Container (React/Streamlit)
└── PostgreSQL Container
```

## Monitoring & Logging

### Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- LLM API call logging

### Metrics (Future)
- Request latency
- Error rates
- LLM API usage
- Database performance

## Technology Stack Summary

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: python-jose, passlib
- **LLMs**: Groq, Google Gemini
- **Testing**: pytest

### Frontend
- **React**: React 18, React Router, Material-UI
- **Streamlit**: Streamlit, Plotly
- **HTTP Client**: Axios / Requests

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Database Migrations**: Alembic
- **Environment**: pydantic-settings, python-dotenv

## Future Enhancements

1. **Redis Caching**: Cache LLM responses and sessions
2. **WebSockets**: Real-time quiz updates
3. **Background Jobs**: Celery for long-running tasks
4. **CDN**: Static asset delivery
5. **Monitoring**: Prometheus + Grafana
6. **CI/CD**: GitHub Actions pipeline
7. **Multi-tenancy**: Organization support
8. **Advanced Analytics**: Learning analytics dashboard
