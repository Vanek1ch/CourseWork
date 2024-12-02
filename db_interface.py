from sqlmodel import SQLModel, Field, Session
from sqlalchemy import create_engine, text
from datetime import date
from sqlalchemy.orm import sessionmaker
import uuid


class Database:
    
    def __init__(self):
        sqlite_file_name = "database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        connect_args = {"check_same_thread": False}
        self.engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=Session)
    
    def get_session(self):
        return self.SessionLocal()
            
    class ItemDB(SQLModel, table=True):
        id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
        market_id: uuid.UUID = Field(default_factory=uuid.uuid4)
        order_id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key='orderdb.id', ondelete="CASCADE")
        name: str
        desc: str | None
        cost: float
        count: int

    class OptionalParametersDB(SQLModel, table=True):
        item_id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="itemdb.id", ondelete="CASCADE")
        id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
        name: str
        value: str
        desc: str | None

    class OrderDB(SQLModel, table=True):
        query_id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="querydb.id", ondelete="CASCADE")
        #order
        id: uuid.UUID = Field(default = None, primary_key=True)
        status: str
        desc: str|None
        #client
        client_id: uuid.UUID = Field(default_factory=uuid.uuid4)
        client_name: str
        client_email: str
        #payment
        payment_status: str
        payment_type: str
        payment_currency: str
        #dest_params
        creation_date: date
        destination_date: date
        destination_type: str
        destination_address: str

    class QueryDB(SQLModel, table=True):
        id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
        company_name: str
        
    def init_db(self):
        SQLModel.metadata.create_all(self.engine, checkfirst=True)
        with self.engine.connect() as connection:
            connection.execute(text("PRAGMA journal_mode=WAL"))
            connection.execute(text("PRAGMA foreign_keys=ON"))

    def return_engine(self):
        return self.engine