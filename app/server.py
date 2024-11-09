from fastapi import FastAPI, HTTPException, Body, status
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Any
from datetime import date
# Название модуля
app = FastAPI()

# Принятие заказа
# BODY запрос JSON с методом POST по адресу localhost:8000/add-order/
example = {
    "company_name": "OZON",
    "query_id": "1234567890123456",
    "orders": [
        {
            "order_id": "12345678",
            "order_status": "In delivery",
            "order_desc": "Postychat v dver",
            "order_dest_desc": {
                "creation_date": "2024-11-09",
                "destination_date": "2024-12-01",
                "destination_type": "Courier",
                "destionation_address": "Bebrovskya 15"
            },
            "order_pay_desc": {
                "payment_status": "Already",
                "payment_type": "Online",
                "payment_currency": "rub"
            },
            "client_desc": {
                "client_id": "12345678",
                "client_name": "Ivan",
                "client_email": "Bebra@mail.ru"
            },
            "order_items": {
                "items": [
                    {
                        "item_id": "12345678",
                        "item_name": "Krossovki naike",
                        "item_desc": "Krosovki naike original real'no",
                        "item_cost": "1200",
                        "optional_parametres": {
                            "size": "45"
                        },
                        "item_count": "1"
                    },
                    {
                        "item_id": "12345178",
                        "item_name": "Krossovki naike2",
                        "item_desc": "Krosovki naike2 original real'no",
                        "item_cost": "1200",
                        "optional_parametres": {
                            "size": "35"
                        },
                        "item_count": "21"
                    }
                ]
            }
        }
    ],
    "query_params": {
        "bebra": "True"
    }
}

# Описание класса Item, товары, которые пользователь приобретает
class Item(BaseModel):
    item_id: str  = Field(pattern=r"\d{8}",max_length=8)
    item_name: str = Field(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    item_desc: str | None = Field(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)
    item_cost: str = Field(pattern=r"(^[\d],\d{1,50})|([^0]\d{1,50})", max_length=50)
    optional_parametres: dict | None = None
    # Добавить обработку ошибки с минусом в кол-ве
    item_count: str = Field(pattern=r"\d{1,2}", max_length=2)

class OrderItems(BaseModel):
    items: list[Item]

class ClientDesc(BaseModel):
    client_id: str = Field(pattern=r"\d{8}", max_length=8)
    client_name: str = Field(pattern=r"[a-zA-Z|\d]{3,50}", max_length=50)
    client_email: EmailStr

class OrderPayDesc(BaseModel):
    payment_status: str = Field(pattern=r"Already|Still", max_length=7)
    payment_type: str = Field(pattern=r"Online|Offline", max_length=7)
    payment_currency: str = Field(pattern=r"dol|rub|eur", max_length=3)

class OrderDestDesc(BaseModel):
    creation_date: date
    destination_date: date
    destination_type: str = Field(pattern=r"Courier|pick-up point", max_length=13)
    destionation_address: str = Field(pattern=r"[a-zA-Z|\d\s]{5,250}", max_length=250)


class Order(BaseModel):
    order_id: str = Field(pattern=r"\d{8}", max_length=8)
    order_status: str = Field(pattern=r"Success|In delivery|Canceled|Not paid", max_length=11)
    order_desc: str | None = Field(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)
    order_dest_desc: OrderDestDesc | None = None
    order_pay_desc: OrderPayDesc | None = None
    client_desc: ClientDesc | None = None
    order_items: OrderItems | None = None


class Query(BaseModel):
    company_name: str = Field(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    query_id: str = Field(pattern=r"\d{16}", max_length=16)
    orders: list[Order]
    query_params: dict[str, bool]


@app.post("/add-order/", response_model_exclude_unset=True)
async def add_order(query: Annotated[Query, Body(embed=True)]) -> Query:
    return query

# 1 проверка на работу класса Item
#@app.post("/item-test/", response_model=Item, response_model_exclude_unset=True)
#async def test_item(item: Annotated[Item, Body(embed=True)], ) -> Item:
#    if item.item_count[0] == "-":
#        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Be sure you are not using negative digits.")
#    return item

# 2 проверка на работу класса OrderItems 
#@app.post("/item-test/", response_model_exclude_unset=True)
#async def test_item(order_items: Annotated[OrderItems, Body(embed=True)], ) -> OrderItems:
#    if order_items.items.item_count[0] == "-":
#        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Be sure you are not using negative digits.")
#    return order_items