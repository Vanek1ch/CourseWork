from fastapi import FastAPI, HTTPException, Body, status, Depends, Query as QueryF
from pydantic import Field as FieldP, EmailStr, BaseModel
from sqlmodel import Session, select
from uuid import uuid1, uuid4, UUID
from random import randint
from typing import Annotated, Any
from datetime import date
from db_interface import Database
# Название модуля
app = FastAPI()

# Принятие заказа
# BODY запрос JSON с методом POST по адресу localhost:8000/add-order/
# Запуск БД
Controller = Database()
Controller.init_db()

engine = Controller.return_engine() 

def get_session():
    with Session(engine) as session:
        yield session 
        
class OptionalParameters(BaseModel):
    name: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    value: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)

# Описание класса Item, товары, которые пользователь приобретает
class Item(BaseModel):
    id: UUID = FieldP(default=None)
    market_id: UUID
    name: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)
    cost: float
    optional_parameters: list[OptionalParameters]
    # Добавить обработку ошибки с минусом в кол-ве
    count: str = FieldP(pattern=r"\d{1,2}", max_length=2)

class Order(BaseModel):
    #order
    id: UUID | None = FieldP(default=None)
    status: str = FieldP(pattern=r"Success|In delivery|Canceled|Not paid", max_length=11)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)
    #client
    client_id: UUID
    client_name: str = FieldP(pattern=r"[a-zA-Z|\d]{3,50}", max_length=50)
    client_email: EmailStr
    #payment
    payment_status: str = FieldP(pattern=r"Already|Still", max_length=7)
    payment_type: str = FieldP(pattern=r"Online|Offline", max_length=7)
    payment_currency: str = FieldP(pattern=r"dol|rub|eur", max_length=3)
    #dest_parameters
    creation_date: date
    destination_date: date
    destination_type: str = FieldP(pattern=r"Courier|pick-up point", max_length=13)
    destination_address: str = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", max_length=250)
    #items
    items: list[Item]

class QueryBase(BaseModel):
    company_name: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    id: UUID | None = FieldP(default=None)
class Query(QueryBase):
    orders: list[Order] | None
    params: dict[str, bool] | None = None

@app.post("/add-query/", response_model=QueryBase)
async def add_query(
    query: Annotated[Query, Body()],
    session: Session = Depends(get_session)
):
    # Для запроса 
    if query.id is None:
        id = uuid4()
        query.id = id
    db_query = Database.QueryDB.model_validate(query)

    # Для заказа 
    orders = query.orders
    for order in orders:
        if order.id is None:
            id = uuid4()
            order.id = id
        #for item in order.items:
        #    db_item.order_id = order.id
        #   db_item = Database.ItemDB.model_validate(item)
        #    session.add(db_item)
        db_order = Database.OrderDB.model_validate(order)
        db_order.query_id = query.id
        print(db_order)
        session.add(db_order)
    
    # Для предметов
    for order in orders:
        for item in order.items:
            if item.id is None:
                id = uuid4()
                item.id = id
            db_item = Database.ItemDB.model_validate(item)
            db_item.order_id = order.id
            session.add(db_item)
    
    # Для опций
    for order in orders:
        for item in order.items:
            for optional_parameter in item.optional_parameters:
                db_op = Database.OptionalParametersDB.model_validate(optional_parameter)
                session.add(db_op)
                


    # Коммиты в дб
    session.add(db_query)
    session.commit()
    return query

@app.delete("/delete-query/")
async def add_query(
    query_id: Annotated[UUID, Body(embed=True)],
    session: Session = Depends(get_session)
):
    query = session.get(Database.QueryDB, query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    session.delete(query)
    session.commit()
    return {f"{query_id}": "запрос успешно удален"}