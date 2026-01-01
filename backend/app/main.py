import sys
import io

# Fix Windows console encoding to support Unicode characters
# if sys.platform == "win32":
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
#     sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import case_search, document_drafting, legal_research, statute_search, news_and_cases, document_review
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title="LegalMitra API",
    version="1.0.0",
    description="Backend API for LegalMitra – AI‑powered Indian legal assistant.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def root_health() -> dict:
    """Simple health‑check endpoint."""
    return {"status": "ok", "service": "legalmitra-api"}


# Mount feature routers under /api/v1
app.include_router(legal_research.router, prefix="/api/v1", tags=["legal-research"])
app.include_router(
    document_drafting.router, prefix="/api/v1", tags=["document-drafting"]
)
app.include_router(case_search.router, prefix="/api/v1", tags=["case-search"])
app.include_router(statute_search.router, prefix="/api/v1", tags=["statute-search"])
app.include_router(news_and_cases.router, prefix="/api/v1", tags=["news-and-cases"])
app.include_router(document_review.router, prefix="/api/v1", tags=["document-review"])

# --- Advocate Diary Feature ---
from app.api import diary
from app.core.database import engine
from app.models import diary as diary_models

# Create DB tables
diary_models.Base.metadata.create_all(bind=engine)

app.include_router(diary.router, prefix="/api/v1/diary", tags=["diary"])


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


