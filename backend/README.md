# LegalMitra Backend

AI-powered Legal Assistant Backend API

## Quick Start

1. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
copy .env.example .env
# Edit .env and add your API keys
```

4. **Run server:**
```bash
python -m app.main
# Or
uvicorn app.main:app --reload --port 8888
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/legal-research` - Legal research queries
- `POST /api/v1/draft-document` - Document drafting
- `POST /api/v1/search-cases` - Case law search
- `POST /api/v1/search-statute` - Statute search

## API Documentation

Once server is running, visit:
- Swagger UI: http://localhost:8888/docs
- ReDoc: http://localhost:8888/redoc

> **Note**: Default port is 8888. Change `PORT` in `.env` file to use a different port.

