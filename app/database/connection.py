import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    
    if not url:
        raise ValueError("DATABASE_URL not found!")
    return url


engine = create_engine(get_database_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    return SessionLocal()

