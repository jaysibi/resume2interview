from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database connection string
POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/resumetailor"
)

# Create engine with connection pooling configuration
engine = create_engine(
    POSTGRES_URL,
    pool_size=20,              # Maximum number of connections in the pool
    max_overflow=10,           # Maximum overflow connections beyond pool_size
    pool_timeout=30,           # Timeout in seconds for getting a connection from the pool
    pool_recycle=3600,         # Recycle connections after 1 hour (3600 seconds)
    pool_pre_ping=True,        # Verify connection health before using
    echo=False,                # Set to True to log all SQL statements (useful for debugging)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
