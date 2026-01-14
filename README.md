# WikiSmart-Edu

**An intelligent educational platform for learning from Wikipedia articles**

## Overview

WikiSmart-Edu is an innovative educational platform that helps users learn efficiently from Wikipedia articles. The platform offers:

- 📝 **Smart Summarization**: Get concise summaries of Wikipedia articles
- 🌍 **Multi-language Translation**: Translate content to your preferred language (FR, EN, AR, ES, etc.)
- ❓ **Interactive Quizzes**: Auto-generated MCQs and open-ended questions
- 📊 **Progress Tracking**: Monitor your learning journey with detailed analytics
- 📥 **Export Options**: Download summaries and quizzes as PDF or TXT files

## Architecture

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: OAuth 2.0 + JWT
- **LLM Integration**:
  - Groq (for summarization)
  - Google Gemini (for translation and quiz generation)
- **Content Extraction**: Wikipedia API + LangChain (for PDFs)

### Frontend Options
- **React.js**: Modern SPA with Material-UI
- **Streamlit**: Quick prototyping and data visualization

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database Migrations**: Alembic
- **Testing**: pytest with mocked LLM APIs

## Project Structure

```
WikiSmart-Edu/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic & LLM services
│   │   ├── core/             # Security & configuration
│   │   ├── middleware/       # Error handling & logging
│   │   └── utils/            # Validators & helpers
│   ├── tests/                # Unit & integration tests
│   ├── alembic/              # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── react-app/            # React frontend
│   └── streamlit-app/        # Streamlit alternative
├── docker-compose.yml
└── docs/
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+ (for React)
- PostgreSQL 15+

### Environment Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd WikiSmart-Edu
```

2. **Configure environment variables**
```bash
cp backend/.env.example backend/.env
# Edit .env with your API keys and configuration
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Access the application**
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- React Frontend: http://localhost:3000
- Streamlit Frontend: http://localhost:8501

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### React Frontend
```bash
cd frontend/react-app
npm install
npm start
```

#### Streamlit Frontend
```bash
cd frontend/streamlit-app
pip install -r requirements.txt
streamlit run app.py
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Content Processing
- `POST /api/v1/content/summarize` - Summarize article
- `POST /api/v1/content/translate` - Translate content
- `POST /api/v1/content/export/pdf` - Export as PDF
- `POST /api/v1/content/export/txt` - Export as TXT

### Quiz
- `POST /api/v1/quiz/generate` - Generate quiz
- `POST /api/v1/quiz/submit` - Submit quiz answers
- `GET /api/v1/quiz/results/{id}` - Get quiz results

### User
- `GET /api/v1/users/profile` - Get user profile
- `GET /api/v1/users/history` - Get article history

### Admin
- `GET /api/v1/admin/statistics` - Get platform statistics
- `GET /api/v1/admin/users` - Manage users

## Database Schema

### Users Table
- id, username, email, hashed_password, role, created_at

### Articles Table
- id, user_id, url, title, action, created_at

### Quiz Attempts Table
- id, user_id, article_id, score, submitted_at

## Testing

```bash
cd backend
pytest tests/ -v
```

## Features

### User Roles

**Regular User**:
- Summarize, translate, and generate quizzes
- Export content as PDF/TXT
- View personal history and scores

**Administrator**:
- Access global statistics
- Manage user accounts
- View platform analytics

### LLM Configuration

Each LLM service is configured with:
- Temperature: Controls randomness
- Max tokens: Limits response length
- Custom prompts: Task-specific instructions

## Contributing

See [SETUP.md](docs/SETUP.md) for detailed development setup instructions.

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
