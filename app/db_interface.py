from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import date
from typing import Annotated

""" Пример базы данных:
create database queries;
use queries;

create table query (
	query_id int primary key,
	company_name varchar
);
create table orders (
	order_id int primary key,
	order_status varchar,
	order_desc varchar,
); 
create table query_orders(
    query_id fk -> query(query_id),
    order_id fk -> orders(order_id)
);

create table order_dest_desc (
	order_id int fk -> order(order_id),
	creation_date date,
	destination_date date,
	destination_address varchar
);
create table order_pay_desc (
	order_id int fk -> order(order_id),
	payment_status varchar,
	payment_type varchar,

	payment_currency varchar
);
create table client_desc (
	order_id int fk -> order(order_id),
	client_id int,
	client_name varchar,
	client_email varchar
);
create table order_items (
	order_id int fk -> order(order_id),
	item_id int pk
);

create table items (
	item_id int pk,
	item_name varchar,
	item_desc varchar,
	item_cost varchar
);

create table items_opt_parm (
	item_id int fk ->items(item_id),
	parameter_id int fk -> optional_parameters(parameter_id)
);

create table optional_parameters
	parameter_id int pk,
	parameter_name varchar,
	parameter_value varchar
);
"""
class Database:
    class Query(SQLModel, table = True):
        query_id: str = Field(primary_key=True)
        company_name: str

    class Orders(SQLModel, table = True):
        order_id: str = Field(primary_key=True)
        query_id: str = Field(foreign_key="query.query_id")
        order_status: str 
        order_desc: str

    class OrderDestDesc(SQLModel, table = True):
        order_dest_desc: str = Field(primary_key=True)
        order_id: str = Field(foreign_key="orders.order_id")
        creation_date: date
        destination_date: date
        destination_address: str

    class OrderPayDesc(SQLModel, table = True):
        order_pay_desc: str = Field(primary_key=True)
        order_id: str = Field(foreign_key="orders.order_id")
        payment_status: str
        payment_type: str
        payment_currency: str

    class ClientDesc(SQLModel, table = True):
        client_desc: str = Field(primary_key=True)
        order_id: str = Field(foreign_key="orders.order_id")
        client_id: str
        client_name: str
        client_email: str

    class Items(SQLModel, table = True):
        item_id: str = Field(primary_key=True)
        item_name: str 
        item_desc: str
        item_cost: str
    class OrderItems(SQLModel, table = True):
        order_items_id: str | None = Field(primary_key=True, default= None)
        order_id: str = Field(foreign_key="orders.order_id")
        item_id: str = Field(foreign_key="items.item_id")
        
    class OptionalParameters(SQLModel, table = True):
        parameter_id: str | None = Field(primary_key=True, default= None)
        parameter_name: str
        parameter_value: str
        
    class ItemsParameters(SQLModel, table = True):
        item_parameters_id: str | None = Field(primary_key=True, default = None)
        item_id: str = Field(foreign_key="items.item_id")
        parameter_id: str = Field(foreign_key="optionalparameters.parameter_id")

class DatabaseController:
    def __init__(self):
        sqlite_file_name = "database.db"
        self.sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(self.sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)

    def add_query(self, query):
        try:
            with Session(self.engine) as session:
                statement = select(Database.Query).where(Database.Query.query_id == query.query_id)
                result = session.exec(statement)
                if result.first():
                    return "Already exists"
                else:
                    query_now = Database.Query(query_id=query.query_id, company_name=query.company_name)
                    
                    return None
        except Exception as e:
            return e