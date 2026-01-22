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
import logging

logger = logging.getLogger(__name__)

# FIX: Validate AI_PROVIDER at startup - fail fast only if provider is invalid
# API key validation happens lazily when AI service is actually used
try:
    settings = get_settings()
    # Only validate that AI_PROVIDER is set and valid (not empty/invalid)
    VALID_PROVIDERS = {"gemini", "openai", "anthropic", "grok", "zai", "openrouter"}
    raw_provider = settings.AI_PROVIDER.strip().lower() if settings.AI_PROVIDER else ""
    
    if not raw_provider:
        logger.warning("AI_PROVIDER is not set - using default 'anthropic'")
    elif raw_provider not in VALID_PROVIDERS and raw_provider != "google":
        error_msg = (
            f"Invalid AI_PROVIDER='{settings.AI_PROVIDER}'. "
            f"Must be one of {sorted(VALID_PROVIDERS)}. "
            f"App cannot start with invalid AI_PROVIDER."
        )
        logger.critical(error_msg)
        print(f"❌ {error_msg}")
        raise RuntimeError(error_msg)
    else:
        logger.info(f"✅ AI_PROVIDER validated: {raw_provider if raw_provider != 'google' else 'gemini'}")
    
    # Import AI service (will validate API keys lazily when used)
    from app.services.ai_service import ai_service
    logger.info("✅ AI service module loaded successfully")
except RuntimeError:
    # Re-raise RuntimeError (invalid provider)
    raise
except Exception as e:
    # Log other errors but don't prevent app from starting
    error_msg = f"Warning during AI service import: {e}"
    logger.warning(error_msg, exc_info=True)
    print(f"⚠️ {error_msg} - App will start but AI features may not work")

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
    
    FIX 5: Includes AI readiness status for production monitoring.
    """
    from datetime import datetime
    import os
    import gc
    
    # Force garbage collection on Render to free memory
    if os.getenv('RENDER'):
        gc.collect()
    
    # FIX 5: Check AI service readiness
    ai_ready = False
    ai_provider = None
    try:
        from app.services.ai_service import ai_service
        from app.core.config import get_settings
        settings = get_settings()
        ai_provider = settings.AI_PROVIDER.lower().strip()
        
        # Check if the selected provider's client is available
        if ai_provider == "gemini":
            # For Gemini, check if client can be initialized (lazy loading)
            if hasattr(ai_service, '_gemini_client') and ai_service._gemini_client is not None:
                ai_ready = True
            elif hasattr(ai_service, '_gemini_init_error') and ai_service._gemini_init_error:
                ai_ready = False  # Has error
            else:
                # Try to initialize to check readiness
                try:
                    ai_service._initialize_gemini_client()
                    ai_ready = ai_service._gemini_client is not None
                except:
                    ai_ready = False
        elif ai_provider == "anthropic":
            ai_ready = hasattr(ai_service, '_anthropic_client') and ai_service._anthropic_client is not None
        elif ai_provider == "openai":
            ai_ready = hasattr(ai_service, '_openai_client') and ai_service._openai_client is not None
        else:
            ai_ready = True  # Other providers (grok, zai, openrouter) - assume ready if no error
    except Exception as e:
        # If AI service check fails, log but don't fail health check
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"AI readiness check failed: {e}")
        ai_ready = False
    
    return {
        "status": "ok",
        "service": "legalmitra-api",
        "timestamp": datetime.now().isoformat(),
        "uptime_check": "healthy",
        "ai_provider": ai_provider or "unknown",
        "ai_ready": ai_ready
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


