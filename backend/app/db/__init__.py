from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from urllib.parse import quote_plus
from app.config import DATABASE as db_info
from colorama import Fore

encoded_password = quote_plus(str(db_info.get('password') or ''))
DATABASE_URL = f"postgresql://{db_info['username']}:{encoded_password}@{db_info['host']}:{db_info['port']}/{db_info['database']}"

Base = declarative_base()

_engine = None

def get_db_engine():
    global _engine
    if _engine is None:
        try:
            _engine = create_engine(DATABASE_URL, echo=False)
        except Exception as e:
            print(f"{Fore.RED}Error creating database engine: {e}{Fore.WHITE}")
            return None
    return _engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_db_engine())

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a request-scoped SQLAlchemy Session.
    
    Each incoming request receives a dedicated Session that is guaranteed to be
    closed when the request finishes, preventing session leaks and concurrency race conditions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session() -> Session:
    """Standalone session provider for non-request scripts (e.g., database seeders).
    
    Callers are responsible for closing the returned session.
    """
    return SessionLocal()

def create_tables():
    try:
        engine = get_db_engine()
        if engine is not None:
            Base.metadata.create_all(bind=engine)
            print("Database tables initialized successfully.")
    except Exception as e:
        print(f"{Fore.RED}Failed to connect to database or create tables: {e}{Fore.WHITE}")
        print(f"{Fore.YELLOW}Tip: Check POSTGRES_PASSWORD and POSTGRES_DB in backend/.env{Fore.WHITE}")
