from typing import Annotated
from fastapi import Depends
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

def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session

# Session Dependency Annotation
SessionDep = Annotated[Session, Depends(get_session)]
