from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables!")

# Base class for defining models
Base = declarative_base()

# Factory to create the database engine
def create_db_engine(database_url=DATABASE_URL):
    return create_engine(database_url)

# Create the SQLAlchemy engine
engine = create_db_engine()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for retrieving a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
