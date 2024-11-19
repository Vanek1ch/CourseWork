from fastapi import Depends, FastAPI, HTTPException, Query, Body
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from pydantic import Field as FieldP, EmailStr
from typing import Annotated
from datetime import date

class Item(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    name: str 
    desc: str 
    cost: float
    count: int
    optional_parameters: list['OptionalParameters'] = Relationship(back_populates="item")
    order_id: int = Field(default=None, foreign_key="order.id")
    order_items: 'Order' = Relationship(back_populates="items_order")

class OptionalParameters(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    value: str
    item_id: int = Field(default=None, foreign_key="item.id")
    item: Item = Relationship(back_populates="optional_parameters")


class QueryBase(SQLModel):
    company_name: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    id: int = Field(default=None, primary_key=True)
    

class Query(QueryBase, table=True):
    orders: list['Order'] | None = Relationship(back_populates="query")

class QueryPublic(QueryBase):
    pass

class Order(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    status: str = FieldP(pattern=r"Success|In delivery|Canceled|Not paid", max_length=11)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)
    #Client
    client_id: str = FieldP(pattern=r"\d{8}", max_length=8)
    client_name: str = FieldP(pattern=r"[a-zA-Z|\d]{3,50}", max_length=50)
    client_email: EmailStr
    #Payment
    payment_status: str = FieldP(pattern=r"Already|Still", max_length=7)
    payment_type: str = FieldP(pattern=r"Online|Offline", max_length=7)
    payment_currency: str = FieldP(pattern=r"dol|rub|eur", max_length=3)
    #Date
    creation_date: date
    destination_date: date
    destination_type: str = FieldP(pattern=r"Courier|pick-up point", max_length=13)
    destionation_address: str = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", max_length=250)
    #relations
    query_id: int = Field(foreign_key="query.id")
    query: Query = Relationship(back_populates="orders")
    items_order: list['Item'] | None = Relationship(back_populates="order_items")

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.post("/query-create/", response_model=QueryPublic)
def query_create(
    query: Annotated[Query, Body],
    order: Annotated[Order, Body],
    #items: Annotated[Item, Body],
    #optional_parameters: Annotated[OptionalParameters, Body],
    session: Session = Depends(get_session)) -> QueryPublic:
    db_query = query
    db_query.orders = order
    #db_query.orders.items_order = items
    #db_query.orders.items.optional_parameters = optional_parameters
    db_query = Query.model_validate(query)
    session.add(db_query)
    session.commit()
    session.refresh(db_query)
    return db_query