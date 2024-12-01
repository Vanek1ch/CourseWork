# -*- coding: utf-8 -*-
from model_forms import *
from fastapi import FastAPI, HTTPException, Body, Depends, Query as QueryF, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlmodel import Session, select
from uuid import uuid4
from typing import Annotated, Any
from db_interface import Database

# module name
app = FastAPI()

# bd init
Controller = Database()
Controller.init_db()

engine = Controller.return_engine() 

# func to get session
def get_session():
    with Session(engine) as session:
        yield session 


# adding a query with POST method 
@app.post("/add-query/")
async def add_query(
    query: Annotated[Query, Body()],
    session: Session = Depends(get_session)
)-> Any:
    
    # getting an query if exists
    query_get = session.get(Database.QueryDB, query.id)
    if query_get:
        return JSONResponse(status_code=409, content=jsonable_encoder(f"Запрос с id {query.id} уже существует."))
    else:
        try:
            # for query
            if query.id is None:
                id = uuid4()
                query.id = id
                db_query = Database.QueryDB.model_validate(query)
                session.add(db_query)
                
            elif query.id:
                db_query = Database.QueryDB.model_validate(query)
                session.add(db_query)
                
            # for orders
            orders = query.orders
            
            if orders:
                
                for order in orders:
                    
                    order_get = session.get(Database.OrderDB, order.id)
                    
                    if not order_get:
                        
                        if order.id is None:
                            id = uuid4()
                            order.id = id
                            db_order = Database.OrderDB.model_validate(order)
                            db_order.query_id = query.id
                            session.add(db_order)
                            
                        elif order.id:
                            db_order = Database.OrderDB.model_validate(order)
                            db_order.query_id = query.id
                            session.add(db_order)
                    
                    elif order_get:
                        raise HTTPException(status_code=409)
                
                # for items
                for order in orders:
                    
                    if order.items:
                    
                        for item in order.items:
                                
                            item_get = session.get(Database.ItemDB, item.id)
                            
                            if not item_get:
                            
                                if item.id is None:
                                    id = uuid4()
                                    item.id = id
                                    db_item = Database.ItemDB.model_validate(item)
                                    db_item.order_id = order.id
                                    session.add(db_item)
                                
                                elif item.id:
                                    db_item = Database.ItemDB.model_validate(item)
                                    db_item.order_id = order.id
                                    session.add(db_item)
                            
                            elif item_get:
                                raise HTTPException(status_code=409)
                                        
                # Для опций
                for order in orders:
                    
                    if order.items:
                    
                        for item in order.items:
                            
                            if item.optional_parameters:
                            
                                for optional_parameter in item.optional_parameters:
                                    
                                    op_get = session.get(Database.OptionalParametersDB, optional_parameter.id)
                                    
                                    if not op_get:
                                        
                                        if not optional_parameter.id:
                                            id = uuid4()
                                            optional_parameter.id = id
                                            db_op = Database.OptionalParametersDB.model_validate(optional_parameter)
                                            db_op.item_id = item.id
                                            session.add(db_op)
                                        
                                        elif optional_parameter.id:
                                            db_op = Database.OptionalParametersDB.model_validate(optional_parameter)
                                            db_op.item_id = item.id
                                            session.add(db_op)
                                    
                                    elif op_get:
                                        raise HTTPException(status_code=409)
                session.commit()
                
            elif not orders:
                session.commit()
                                                
        except HTTPException as err:
            session.close()
            return JSONResponse(status_code=409, content=f"Ошибка в присваивании id, error {err}")
        
        query_get = session.get(Database.QueryDB, query.id)
        return JSONResponse(status_code=201, content=jsonable_encoder(query_get))

# Удаление запроса
@app.delete("/delete-query/{query_id}")
async def delete_query(
    query_id: Annotated[UUID, Path()],
    session: Session = Depends(get_session)
):
    query = session.get(Database.QueryDB, query_id)
    if not query:
        return JSONResponse(status_code=404, content={f'{query_id}':"Запрос не найден"})
    session.delete(query)
    session.commit()
    return JSONResponse(status_code=200, content={f"{query_id}" : "Запрос успешно удален"})

@app.delete("/delete-order/{order_id}")
async def delete_order(
    order_id: Annotated[UUID, Path()],
    session: Session = Depends(get_session)
):
    get_order = session.get(Database.OrderDB, order_id)
        
    if get_order:
            
        session.delete(get_order)
        session.commit()
        
        return JSONResponse(status_code=200, content=f'Заказ с id: {order_id} успешно удален')
        
    else:
        
        return JSONResponse(status_code=404, content=f"Заказ с id: {order_id} не найден")
    

@app.delete("/delete-item/{item_id}")
async def delete_item(
    item_id: Annotated[UUID, Path()],
    session: Session = Depends(get_session)
):
    get_item = session.get(Database.ItemDB, item_id)
        
    if get_item:
            
        session.delete(get_item)
        session.commit()
        
        return JSONResponse(status_code=200, content=f'Заказ с id: {item_id} успешно удален')
        
    else:
        
        return JSONResponse(status_code=404, content=f"Заказ с id: {item_id} не найден")

@app.delete("/delete-op/{op_id}")
async def delete_op(
    op_id: Annotated[UUID, Path()],
    session: Session = Depends(get_session)
):
    get_op = session.get(Database.OptionalParametersDB, op_id)
        
    if get_op:
            
        session.delete(get_op)
        session.commit()
        
        return JSONResponse(status_code=200, content=f'Заказ с id: {op_id} успешно удален')
        
    else:
        
        return JSONResponse(status_code=404, content=f"Заказ с id: {op_id} не найден")

# Обновление запроса
@app.patch("/update-orders/")
async def update_orders(
    query_id: Annotated[UUID, Body(embed=True)],
    orders: Annotated[list[OrderUpdate], Body(embed=True)],
    session: Session = Depends(get_session)
):
    successful_orders = []
    unsuccessful_orders = []
    
    db_query = session.get(Database.QueryDB, query_id)
    if not db_query:
        return JSONResponse(status_code=404, content=jsonable_encoder( f"Запроса с id: {query_id} не существует!"))
    else:
        for order in orders:
            
            if not order.id:
                id = uuid4()
                order.id = id
                db_order = Database.OrderDB.model_validate(order)
                db_order.query_id = query_id
                session.add(db_order)
                session.commit()
                successful_orders.append(order.id)
            
            elif order.id:
                order_get = session.get(Database.OrderDB, order.id)
                
                if not order_get:
                    unsuccessful_orders.append(order.id)
                
                elif order_get:
                    order_data = order.model_dump(exclude_unset=True)
                    for key, value in order_data.items():
                        setattr(order_get, key, value)
                    session.add(order_get)
                    session.commit()
                    successful_orders.append(order.id)
    
    return JSONResponse(status_code=200, content=jsonable_encoder(f"Успешно изменены заказы : {successful_orders}, Заказы не были изменены (неверный id):{unsuccessful_orders}"))

@app.patch("/update-items/")
async def update_items(
    order_id: Annotated[UUID, Body(embed=True)],
    items: Annotated[list[UpdateItems], Body(embed=True)],
    session: Session = Depends(get_session)
):
    unsuccessful_items = []
    successful_items = []
    
    
    db_order = session.get(Database.OrderDB, order_id)
    if not db_order:
        return JSONResponse(status_code=404, content=jsonable_encoder(f"Заказа с id: {order_id} не существует!"))
    else:
        for item in items:
            
            if not item.id:
                try:
                    id = uuid4()
                    item.id = id
                    db_item = Database.ItemDB.model_validate(item)
                    db_item.order_id = order_id
                    session.add(db_item)
                    session.commit()
                    successful_items.append(item.id)
                except ValidationError as err:
                    unsuccessful_items.append(item.id)
                    # Добавить обработку ошибки
            
            elif item.id:
                item_get = session.get(Database.ItemDB, item.id)
                
                if not item_get:
                    unsuccessful_items.append(item.id)
                
                elif item_get:
                    item_data = item.model_dump(exclude_unset=True, exclude={'optional_parameters'})
                    for key, value in item_data.items():
                        setattr(item_get, key, value)
                    session.add(item_get)
                    session.commit()
                    successful_items.append(item.id)
            
            if item.id not in unsuccessful_items:
                if item.optional_parameters:
                    # Добавить обработку параметров
                    success_parameters = []   
                    
                    for parameter in item.optional_parameters:
                        if not parameter.id:
                            try:
                                id = uuid4()
                                parameter.id = id
                                db_parameter = Database.OptionalParametersDB.model_validate(parameter)
                                db_parameter.item_id = item.id
                                session.add(db_parameter)
                                session.commit()
                                success_parameters.append(parameter.id)
                            except ValidationError:
                                pass # Добавить обработку ошибки
                        
                        elif parameter.id:
                            parameter_get = session.get(Database.OptionalParametersDB, parameter.id)
                        
                            if not parameter_get:
                                pass
                            
                            elif parameter_get:
                                parameter_data = parameter.model_dump(exclude_unset=True)
                                for key, value in parameter_data.items():
                                    setattr(parameter_get, key, value)
                                session.add(parameter_get)
                                session.commit()
                                success_parameters.append(parameter.id)
                
    return JSONResponse(status_code=200, content=(f"Успешно добавлены/изменены товары {successful_items}, Товары завершившие изменение c ошибкой {unsuccessful_items}"))

@app.get("/getall-queryes/")
async def get_queryes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = QueryF(default=100, le=100)
):
    queryes = session.exec(select(Database.QueryDB).offset(offset).limit(limit)).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(queryes))

@app.get("/get-orders/{query_id}")
async def get_orders(
    query_id: UUID,
    session: Session = Depends(get_session)
):
    query = session.get(Database.QueryDB, query_id)
    if not query:
        return JSONResponse(status_code=404, content=jsonable_encoder(f"Заказов с query_id: {query_id} не существует!"))
    else:
        orders = session.exec(select(Database.OrderDB).where(Database.OrderDB.query_id == query_id)).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(orders))
    
@app.get("/get-query/{q_id}")
async def get_query(*,
    session: Session = Depends(get_session),
    q_id: Annotated[UUID, Path()]
):
    query_get = session.get(Database.QueryDB, q_id)
    
    if not query_get:
        
        return JSONResponse(status_code=404, content=jsonable_encoder(f"Запрос с id {q_id} не существует."))
    
    else:
        
        query_get = query_get.model_dump()
        
        return_query = Query.model_validate(query_get)
        
        
        orders_get = session.exec(select(Database.OrderDB).where(Database.OrderDB.query_id == q_id)).all()
        
        if orders_get:
            
            orders: list[Order] = []
            
            for order in orders_get:
                
                order = order.model_dump()
                
                order = Order.model_validate(order)
                
                items_get = session.exec(select(Database.ItemDB).where(Database.ItemDB.order_id == order.id)).all()
                
                orders.append(order)
                
                if items_get:
                    
                    items: list[Item] = []
                        
                    for item in items_get:
                        
                        item = item.model_dump()
                        
                        for key, value in item.items():
                            
                            item[key] = str(value)
                            
                        item = Item.model_validate(item)
                        
                        items.append(item)
                        
                        op_get = session.exec(select(Database.OptionalParametersDB).where(Database.OptionalParametersDB.item_id == item.id)).all()

                        if op_get:
                            
                            ops: list[OptionalParameters] = []
                            
                            for op in op_get:
                                
                                op = op.model_dump()
                                
                                op = OptionalParameters.model_validate(op)
                                
                                ops.append(op)
                            
                            item.optional_parameters = ops

                    order.items = items
                    
            return_query.orders = orders
            
            return JSONResponse(status_code=200, content=jsonable_encoder(return_query))

        else:
            
            return JSONResponse(status_code=200, content=jsonable_encoder(return_query))
        
        

@app.get("/get-order/{order_id}")
async def get_order(
    order_id: Annotated[UUID, Path()],
    session: Session = Depends(get_session)
):
    get_order = session.get(Database.OrderDB, order_id)
        
    if get_order:
        
        return JSONResponse(status_code=200, content=jsonable_encoder(get_order))
        
    else:
        
        return JSONResponse(status_code=404, content=f"Заказ с id: {order_id} не найден")
    

@app.get("/get-item/{item_id}")
async def get_item(
    item_id: Annotated[UUID, Path()],
    session: Session = Depends(get_session)
):
    get_item = session.get(Database.ItemDB, item_id)
        
    if get_item:
        
        return JSONResponse(status_code=200, content=jsonable_encoder(get_item))
        
    else:
        
        return JSONResponse(status_code=404, content=f"Товар с id: {item_id} не найден")

@app.get("/get-op/{op_id}")
async def get_op(
    op_id: Annotated[UUID, Path()],
    session: Session = Depends(get_session)
):
    get_op = session.get(Database.OptionalParametersDB, op_id)
        
    if get_op:
        
        return JSONResponse(status_code=200, content=jsonable_encoder(get_op))
        
    else:
        
        return JSONResponse(status_code=404, content=f"Заказ с id: {op_id} не найден")
    

@app.get("/get-items/{order_id}")
async def get_items(
    order_id: UUID,
    session: Session = Depends(get_session)
):
    order = session.get(Database.OrderDB, order_id)
    if not order:
        raise HTTPException(status_code=404, detail= f"Товаров с order_id: {order_id} не существует!")
    else:
        items = session.exec(select(Database.ItemDB).where(Database.ItemDB.order_id == order_id)).all()
        items_op = []
        for item in items:
            optional_parameters = session.exec(select(Database.OptionalParametersDB).where(Database.OptionalParametersDB.item_id == item.id)).all()
            items_op.append(["item:",item, "optional_parameters:", optional_parameters])
    return JSONResponse(status_code=200, content=jsonable_encoder(items_op))