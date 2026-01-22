from functools import lru_cache
from pathlib import Path
from typing import Optional
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


# Determine the backend directory (where .env file is located)
# This works whether running from project root or backend directory
_BACKEND_DIR = Path(__file__).parent.parent.parent  # Go up from app/core/config.py to backend/
_ENV_FILE_PATH = _BACKEND_DIR / ".env"
# Fallback: if not found, try relative to current working directory
if not _ENV_FILE_PATH.exists():
    # Try relative to project root (if running from project root)
    _alt_path = Path.cwd() / "backend" / ".env"
    if _alt_path.exists():
        _ENV_FILE_PATH = _alt_path
    else:
        # Last resort: try .env in current directory
        _alt_path = Path.cwd() / ".env"
        if _alt_path.exists():
            _ENV_FILE_PATH = _alt_path


class Settings(BaseSettings):
    """Application configuration loaded from environment variables / .env."""

    # AI provider selection: "gemini", "openai", "anthropic", "grok", "zai", "openrouter"
    # Note: "google" is an alias for "gemini" and will be normalized
    # IMPORTANT: For production, explicitly set AI_PROVIDER in environment variables
    AI_PROVIDER: str = "anthropic"  # Default for local development only

    # API keys (only the one for the selected provider is required)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_GEMINI_API_KEY: Optional[str] = None
    GROK_API_KEY: Optional[str] = None
    ZAI_API_KEY: Optional[str] = None

    # OpenRouter API key (provides access to 200+ models)
    OPENROUTER_API_KEY: Optional[str] = None
    # Model to use when AI_PROVIDER is "openrouter"
    OPENROUTER_MODEL: str = "anthropic/claude-3.5-sonnet"
    
    # Web Search API (for fetching latest legal information)
    GOOGLE_CUSTOM_SEARCH_API_KEY: Optional[str] = None
    GOOGLE_CUSTOM_SEARCH_ENGINE_ID: Optional[str] = None

    # Server configuration
    PORT: int = 8888

    # Paths
    SYSTEM_PROMPT_PATH: Path = Path("app/prompts/legal_system_prompt.txt")

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


