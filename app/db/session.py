from dotenv import dotenv_values
from sqlalchemy import Column, Integer, Sequence, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = dotenv_values(".mysqlenv")

MYSQL_DATABASE = config['MYSQL_DATABASE']
MYSQL_USER = config['MYSQL_USER']
MYSQL_PASSWORD = config['MYSQL_PASSWORD']
DATABASE_HOST = "localhost"


DATABASE_URL  = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{DATABASE_HOST}/{MYSQL_DATABASE}"
# DATABASE_URL = "mysql+pymysql://user:password@localhost/db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()