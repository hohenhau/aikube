# Set up the database connection between FastAPI and PostgreSQL through SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Dependency to provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database URL for PostgreSQL (update with your credentials)
user = 'test_user'
password = 'test_password'
database = 'test_db'
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@postgres:5432/{database}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


