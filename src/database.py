from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# to postgresql pattern - postgresql+psycopg2://user:password@host:port/dbname

# SQLALCHEMY_DATABASE_URL='postgresql+psycopg2://postgres:12345@localhost:5432/notes_db_temp_temp'
# with docker - must use container name
SQLALCHEMY_DATABASE_URL='postgresql+psycopg2://postgres:12345@notes_app_postgres:5432/notes_db'
# old db
# SQLALCHEMY_DATABASE_URL = "sqlite:///./itemsAppWithAuth.db"

# https://stackoverflow.com/questions/54118182/sqlalchemy-not-creating-tables

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()