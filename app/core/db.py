from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import get_settings


#Generates the session from the config files (which takes from .env or docker)
settings = get_settings()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.database_user,
    password=settings.database_password,
    host=settings.database_url,
    port=settings.database_port,
    database=settings.database_name,
)



engine = create_engine(
    DATABASE_URL, 
    echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

#Doesn't declare the base entity
class Base(DeclarativeBase):
    pass

#Exports the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()