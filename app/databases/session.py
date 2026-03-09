from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from .models import Shipment

engine = create_engine(
    url = "sqlite:///app/sqlite.db",
    echo=True,
    connect_args={
        "check_same_thread": False
    },
)

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session

