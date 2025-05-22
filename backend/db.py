from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL with your credentials
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/edocr"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SessionLocal for DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
