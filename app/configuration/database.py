from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import DBSettings

db_settings = DBSettings()

DATABASE_URL = db_settings.DB_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
