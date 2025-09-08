"""Database Implementation."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import POSTGRES_URL

engine = create_engine(POSTGRES_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
