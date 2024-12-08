from sqlmodel import Field, Session
from sqlalchemy import create_engine, event
from datetime import date
from sqlalchemy.orm import sessionmaker
import uuid


class Database:
    def __init__(self, db_path="database.db"):
        sqlite_url = f"sqlite:///{db_path}"
        self.engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})
        event.listen(self.engine, "connect", self.set_sqlite_pragma)

    def set_sqlite_pragma(self, dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.close()

    def get_session(self):
        return Session(self.engine)

    def init_db(self):
        from ..db_sqlite.models.model_forms_bd import SQLModel
        SQLModel.metadata.create_all(self.engine, checkfirst=True)

    def return_engine(self):
        return self.engine