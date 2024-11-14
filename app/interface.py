from datetime import date
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from pydantic import EmailStr
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

"""class Item(SQLModel):
    item_id: str = Field(min_length=8,max_length=8)
    item_name: str = Field(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    item_desc: str | None = Field(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)
    item_cost: str = Field(pattern=r"(^[\d],\d{1,50})|([^0]\d{1,50})", max_length=50)
    optional_parameters: dict | None = None
    # Добавить обработку ошибки с минусом в кол-ве
    item_count: str = Field(pattern=r"\d{1,2}", max_length=2)

class OrderItems(SQLModel):
    items: list[Item]

class ClientDesc(SQLModel):
    client_id: str = Field(pattern=r"\d{8}", max_length=8)
    client_name: str = Field(pattern=r"[a-zA-Z|\d]{3,50}", max_length=50)
    client_email: EmailStr

class OrderPayDesc(SQLModel):
    payment_status: str = Field(pattern=r"Already|Still", max_length=7)
    payment_type: str = Field(pattern=r"Online|Offline", max_length=7)
    payment_currency: str = Field(pattern=r"dol|rub|eur", max_length=3)

class OrderDestDesc(SQLModel):
    creation_date: date
    destination_date: date
    destination_type: str = Field(pattern=r"Courier|pick-up point", max_length=13)
    destionation_address: str = Field(pattern=r"[a-zA-Z|\d\s]{5,250}", max_length=250)
"""



database_url = 'sqlite:///db.sqlite'
engine = create_engine(database_url, echo=True)
def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class OrderBase(SQLModel):
    order_status: str
    order_desc: str | None = None
    query_id: int = Field(foreign_key="query.id")

class Order(OrderBase, table=True):
    id: int = Field(default=None, primary_key=True)
    query: "Query" = Relationship(back_populates="orders")

"""class OrderCreate(OrderBase):
    order_dest_desc: OrderDestDesc | None = None
    order_pay_desc: OrderPayDesc | None = None
    client_desc: ClientDesc | None = None
    order_items: OrderItems | None = None"""

class QueryBase(SQLModel):
    company_name: str

class Query(QueryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    orders: list[Order] = Relationship(back_populates="query")

class QueryCreate(QueryBase):
    orders: list[OrderBase] = []
    query_params: dict[str, bool] | None = None

@app.post("/query")
async def create_query(
    query_data: QueryCreate,
    session: Session = Depends(get_session)
    ) -> Query:
    query = Query(company_name=query_data.company_name, orders=query_data.orders)
    session.add(query)
    if query_data.orders:
        for order in query_data.orders:
            order_obj = Order(order_status=order.order_status)
    session.commit()
    session.refresh(query)
    return query 