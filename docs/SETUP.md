# Development Setup Guide

## Prerequisites

### Required Software
- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 15 or higher
- Docker & Docker Compose (optional but recommended)
- Git

### API Keys
You'll need API keys for:
- **Groq**: Get from https://console.groq.com/
- **Google Gemini**: Get from https://makersuite.google.com/app/apikey

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/wikismart_db
SECRET_KEY=your-very-secret-key-change-this
GROQ_API_KEY=your-groq-api-key
GEMINI_API_KEY=your-gemini-api-key
```

### 4. Setup Database

```bash
# Create database
createdb wikismart_db

# Run migrations
alembic upgrade head
```

### 5. Run Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## Frontend Setup

### React Frontend

```bash
cd frontend/react-app
npm install
npm start
```

React app will be available at: http://localhost:3000

### Streamlit Frontend

```bash
cd frontend/streamlit-app
pip install -r requirements.txt
streamlit run app.py
```

Streamlit app will be available at: http://localhost:8501

## Docker Setup (Recommended)

### 1. Build and Start All Services

```bash
# From project root
docker-compose up -d --build
```

### 2. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

### 3. Stop Services

```bash
docker-compose down
```

### 4. Reset Everything

```bash
docker-compose down -v  # Remove volumes too
docker-compose up -d --build
```

## Database Migrations

### Create New Migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migration

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Running Tests

### Backend Tests

```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Specific test file
pytest tests/test_auth.py -v
```

### Frontend Tests

```bash
cd frontend/react-app
npm test
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code
- Add tests
- Update documentation

### 3. Run Tests

```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend/react-app
npm test
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: description of your changes"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

## Code Quality

### Python Linting

```bash
cd backend
# Install tools
pip install black flake8 mypy

# Format code
black app/

# Check style
flake8 app/

# Type checking
mypy app/
```

### JavaScript Linting

```bash
cd frontend/react-app
npm run lint
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U user -d wikismart_db -h localhost
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Docker Issues

```bash
# Remove all containers and images
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up -d --build
```

### Module Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

## Environment Variables Reference

### Backend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `SECRET_KEY` | JWT secret key | Yes | - |
| `ALGORITHM` | JWT algorithm | No | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | No | 30 |
| `GROQ_API_KEY` | Groq API key | Yes | - |
| `GROQ_MODEL` | Groq model name | No | mixtral-8x7b-32768 |
| `GROQ_TEMPERATURE` | Groq temperature | No | 0.7 |
| `GROQ_MAX_TOKENS` | Groq max tokens | No | 1024 |
| `GEMINI_API_KEY` | Gemini API key | Yes | - |
| `GEMINI_MODEL` | Gemini model name | No | gemini-pro |
| `GEMINI_TEMPERATURE` | Gemini temperature | No | 0.5 |
| `GEMINI_MAX_TOKENS` | Gemini max tokens | No | 2048 |
| `WIKIPEDIA_USER_AGENT` | Wikipedia API user agent | Yes | - |
| `BACKEND_CORS_ORIGINS` | Allowed CORS origins | No | ["*"] |

## Useful Commands

### Database

```bash
# Backup database
pg_dump wikismart_db > backup.sql

# Restore database
psql wikismart_db < backup.sql

# Reset database
dropdb wikismart_db && createdb wikismart_db
alembic upgrade head
```

### Docker

```bash
# View running containers
docker ps

# Execute command in container
docker exec -it wikismart_backend bash

# View container logs
docker logs wikismart_backend

# Rebuild specific service
docker-compose up -d --build backend
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [React Documentation](https://react.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Groq Documentation](https://console.groq.com/docs)
- [Gemini Documentation](https://ai.google.dev/docs)
