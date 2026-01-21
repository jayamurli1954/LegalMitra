import sys
import io
from pathlib import Path

# Fix Windows console encoding to support Unicode characters
# if sys.platform == "win32":
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
#     sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api import case_search, document_drafting, legal_research, statute_search, news_and_cases, document_review, model_selection, templates, smart_routing, cost_tracking, enhanced_query, legal_templates_v2
from app.core.config import get_settings
from fastapi.staticfiles import StaticFiles

settings = get_settings()


settings = get_settings()

app = FastAPI(
    title="LegalMitra API",
    version="1.0.0",
    description="Backend API for LegalMitra – AI‑powered Indian legal assistant.",
)

# Rate limiting to prevent accidental API abuse
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour", "20/minute"]  # Reasonable limits for personal use
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint removed to allow StaticFiles to serve index.html at /
# @app.get("/")
# async def root() -> dict:
#     ...

@app.get("/health")
async def root_health() -> dict:
    """
    Health check endpoint for monitoring and keep-alive services.
    Used by Render's health checks and external monitoring services.
    """
    from datetime import datetime
    import os
    import gc
    
    # Force garbage collection on Render to free memory
    if os.getenv('RENDER'):
        gc.collect()
    
    return {
        "status": "ok",
        "service": "legalmitra-api",
        "timestamp": datetime.now().isoformat(),
        "uptime_check": "healthy"
    }


# Mount feature routers under /api/v1
app.include_router(legal_research.router, prefix="/api/v1", tags=["legal-research"])
app.include_router(
    document_drafting.router, prefix="/api/v1", tags=["document-drafting"]
)
app.include_router(case_search.router, prefix="/api/v1", tags=["case-search"])
app.include_router(statute_search.router, prefix="/api/v1", tags=["statute-search"])
app.include_router(news_and_cases.router, prefix="/api/v1", tags=["news-and-cases"])
# FIX 6: Lazy-load document_review router to reduce startup memory
def include_document_review_router(app):
    """Lazy load document review router"""
    from app.api import document_review
    app.include_router(document_review.router, prefix="/api/v1", tags=["document-review"])

include_document_review_router(app)
app.include_router(model_selection.router, prefix="/api/v1", tags=["model-selection"])
app.include_router(templates.router, prefix="/api/v1", tags=["templates"])
app.include_router(smart_routing.router, prefix="/api/v1", tags=["smart-routing"])
app.include_router(cost_tracking.router, prefix="/api/v1", tags=["cost-tracking"])
app.include_router(enhanced_query.router, prefix="/api/v1", tags=["enhanced-query"])
app.include_router(legal_templates_v2.router, prefix="/api/v1", tags=["legal-templates-v2"])

# --- Advocate Diary Feature ---
from app.api import diary
from app.core.database import engine
from app.models import diary as diary_models
from app.models import audit_log as audit_models

# Create DB tables
diary_models.Base.metadata.create_all(bind=engine)
audit_models.Base.metadata.create_all(bind=engine)

app.include_router(diary.router, prefix="/api/v1/diary", tags=["diary"])

# Serve Frontend Static Files (Must be last to not block API)
# We assume the app is run from 'backend/' directory, so frontend is at '../frontend'
frontend_path = Path(__file__).parent.parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")


def run() -> None:
    """Entry‑point used by the launcher script: python -m app.main."""
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=False,
    )


if __name__ == "__main__":
    run()


