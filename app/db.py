from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

conn_args = {"check_same_thread":False}
engine = create_engine(sqlite_url, connect_args=conn_args)

def crete_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
    
SessionDep = Annotated[Session, Depends(get_session)]