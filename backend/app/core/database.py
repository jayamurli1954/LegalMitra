from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database file
# Get DATABASE_URL from environment variable, fallback to SQLite for local dev
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./diary.db")

# Handle Heroku/Render-style postgres:// URLs (SQLAlchemy 1.4+ requires postgresql://)
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine
# check_same_thread=False is ONLY needed for SQLite
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    print(f"Database Config: Using SQLite ({SQLALCHEMY_DATABASE_URL})")
else:
    print(f"Database Config: Using PostgreSQL/External ({SQLALCHEMY_DATABASE_URL.split('@')[-1] if '@' in SQLALCHEMY_DATABASE_URL else 'Hidden URL'})")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
