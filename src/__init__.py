import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base class for SQLAlchemy models
Base = declarative_base()

# Database connection URL
DATABASE_URL = os.environ["database_url"]

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to initialize the database (create tables, etc.)
def init_db() -> None:
    from ingestion import models  # Import models to register them with SQLAlchemy  # noqa: F401

    Base.metadata.create_all(bind=engine)
