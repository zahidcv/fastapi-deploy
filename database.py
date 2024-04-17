from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:///blog.db'
SQLALCHEMY_DATABASE_URL = "postgresql://blogger:FzWbeUEVYqux9n4sNBqxl8EcEBhh97gC@dpg-cofvha7sc6pc7382ua90-a.oregon-postgres.render.com/blogdb_brle"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush = False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()

