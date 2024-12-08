from pydantic import Field as FieldP, EmailStr, BaseModel
from uuid import UUID
from datetime import date


############################################################################################################################
                                                #models for server#
############################################################################################################################

# class to set optional parameters (op in next) for items         
class OptionalParameters(BaseModel):
    id: UUID | None = FieldP(default=None)
    name: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    value: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)

# class to update op in UpdateItems class
class OptionalParametersUpdate(BaseModel):
    id: UUID | None = FieldP(default=None)
    name: str | None = FieldP(default=None, pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    value: str | None = FieldP(default=None, pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)

# class to set items for Order class
class Item(BaseModel):
    id: UUID = FieldP(default=None)
    market_id: UUID
    name: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)
    cost: float
    optional_parameters: list[OptionalParameters] | None = FieldP(default=None)
    # Добавить обработку ошибки с минусом в кол-ве
    count: str = FieldP(pattern=r"\d{1,2}", max_length=2)
    
# class to update items for OrderUpdate class
class UpdateItems(BaseModel):
    id: UUID | None = FieldP(default=None)
    market_id: UUID | None = FieldP(default=None)
    name: str | None = FieldP(default=None, pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)
    cost: float | None = FieldP(default=None)
    count: str | None = FieldP(default=None, pattern=r"\d{1,2}", max_length=2)
    optional_parameters: list[OptionalParametersUpdate] | None = FieldP(default=None)

# base class to order where id/status and desc defined (not in use by ourself)
class OrderBase(BaseModel):
    #order
    id: UUID | None = FieldP(default=None)
    status: str = FieldP(pattern=r"Success|In delivery|Canceled|Not paid", max_length=11)
    desc: str | None = FieldP(pattern=r"[a-zA-Z|\d\s]{5,250}", default=None, max_length=250)

# order class using OrderBase, Order using by it's own 
class Order(OrderBase):
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
    items: list[Item] | None = FieldP(None)

# order update class to update orders
class OrderUpdate(BaseModel):
    #order
    id: UUID | None = FieldP(default=None)
    status: str | None = FieldP(default=None, pattern=r"Success|In delivery|Canceled|Not paid", max_length=11)
    desc: str | None = FieldP(default=None, pattern=r"[a-zA-Z|\d\s]{5,250}", max_length=250)
    #client
    client_id: UUID | None = FieldP(default=None)
    client_name: str | None = FieldP(default=None, pattern=r"[a-zA-Z|\d]{3,50}", max_length=50)
    client_email: EmailStr | None = FieldP(default=None)
    #payment
    payment_status: str | None = FieldP(default=None, pattern=r"Already|Still", max_length=7) 
    payment_type: str | None = FieldP(default=None, pattern=r"Online|Offline", max_length=7)
    payment_currency: str | None = FieldP(default=None, pattern=r"dol|rub|eur", max_length=3)
    #dest_parameters
    creation_date: date | None = FieldP(default=None)
    destination_date: date | None = FieldP(default=None)
    destination_type: str | None = FieldP(default=None, pattern=r"Courier|pick-up point", max_length=13)
    destination_address: str | None = FieldP(default=None, pattern=r"[a-zA-Z|\d\s]{5,250}", max_length=250)

# give an desc
class QueryBase(BaseModel):
    id: UUID | None = FieldP(default=None)

# give an desc
class Query(QueryBase):
    company_name: str = FieldP(pattern=r"[a-zA-Z|\d\s]{3,50}", max_length=50)
    orders: list[Order] | None = FieldP(default=None)
    params: dict[str, bool] | None = FieldP(default=None)

############################################################################################################################




############################################################################################################################
                                                #models for desktop app#
############################################################################################################################

class DesktopQuery(Query):
    method: str = FieldP(pattern=r"POST|DELETE|GET", max_length=6)
    object: str = FieldP(pattern=r"Query", max_length=6)
    
class DesktopQueryDelete(BaseModel):
    method: str = FieldP(pattern=r"POST|DELETE|GET", max_length=6)
    object: str = FieldP(pattern=r"Query", max_length=6)
    query_id: UUID

class DesktopOrderDelete(BaseModel):
    method: str = FieldP(pattern=r"POST|DELETE|GET", max_length=6)
    object: str = FieldP(pattern=r"Order", max_length=6)
    order_id: UUID
    
class DesktopItemDelete(BaseModel):
    method: str = FieldP(pattern=r"POST|DELETE|GET", max_length=6)
    object: str = FieldP(pattern=r"Item", max_length=6)
    item_id: UUID

class DesktopOPDelete(BaseModel):
    method: str = FieldP(pattern=r"POST|DELETE|GET", max_length=6)
    object: str = FieldP(pattern=r"OP", max_length=6)
    op_id: UUID