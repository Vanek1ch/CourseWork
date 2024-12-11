from sqlmodel import SQLModel, Field
from datetime import date

import uuid

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