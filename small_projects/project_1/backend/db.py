from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# This is the Connection String.
SQLALCHEMY_DB_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread":False},
)

# It creates DB session, each request will get it's own session.
SessionLocal = sessionmaker(
    autoflush=False, 
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db