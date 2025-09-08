"""Database Implementation."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_URL

# creating the engine
engine = create_engine(POSTGRES_URL)

# creating the session
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# creating what?
Base = declarative_base()
