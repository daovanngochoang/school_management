import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from setting import *

settings: Settings = settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.__str__()
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


