from functools import lru_cache
from pathlib import Path
from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables / .env."""

    # AI provider selection: "anthropic", "openai", "google", "grok"
    AI_PROVIDER: str = "anthropic"

    # API keys (only the one for the selected provider is required)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_GEMINI_API_KEY: Optional[str] = None
    GROK_API_KEY: Optional[str] = None

    # Server configuration
    PORT: int = 8888

    # Paths
    SYSTEM_PROMPT_PATH: Path = Path("app/prompts/legal_system_prompt.txt")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


