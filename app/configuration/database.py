from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import DBSettings, RedisSettings
from redis import Redis

db_settings = DBSettings()
redis_settings = RedisSettings()


engine = create_engine(db_settings.DB_URL, connect_args={"check_same_thread": False})
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Fournit une session de base de données aux dépendances FastAPI.
    Gère automatiquement l'ouverture et la fermeture des connexions.
    """
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


# Initialiser un client Redis avec les configurations
redis_client = Redis(
    host=redis_settings.REDIS_HOST,
    port=redis_settings.REDIS_PORT,
    db=redis_settings.REDIS_DB,
    # password=redis_settings.REDIS_PASSWORD
)


def get_redis():
    """
    Fournit une instance de client Redis aux dépendances FastAPI.
    """
    return redis_client
