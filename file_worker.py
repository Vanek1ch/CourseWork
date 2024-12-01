import os
import json
import mimetypes as mt
import re
import uuid
from pydantic import ValidationError
from model_forms import DesktopQuery, DesktopQueryDelete, DesktopOrderDelete, DesktopItemDelete, DesktopOPDelete, Order, Item, OptionalParameters
from db_interface import Database
from sqlmodel import Session
from db_interface import Database

Controller = Database()
Controller.init_db() # later to delete because of server

engine = Controller.return_engine()

# func to get session
def get_session():
    session = Session(engine)
    return session

""" work in progress 
class QueryesOperator:
    
    def find_query(
        file_data: dict, session: Session, db_class: Database,
        return_model_id: bool | None, is_start_func: bool | None,
        find_model_name: str | None, validation_class: str,
        last_model_id: str | None, last_model_id_name: str | None) -> str | bool:
        
        if is_start_func:
            
            try:
                        
                json_dump = json.dumps(file_data)
                validation_class.model_validate_json(json_dump) # //need to fix model validating
            
            except ValidationError as err:
                session.close()
                print(err)
                return False
            
            q: uuid.UUID = None
            
            # getting query id to get session 
            for key, value in file_data.items():
                
                if key == 'id':
                    
                    q_id = uuid.UUID(value)
            
            q_get = session.get(db_class, q_id)
                    
            if q_get:
                        
                return False
                
            else:
                
                try:
                    
                    obj = db_class.model_validate(file_data)
                                
                    session.add(obj)

                except Exception as e:
                    session.close()
                    print(e)
                    return False
            
            if return_model_id:
                
                return q_id
        
        else:
            
            for key, value in file_data.items():
                
                if key == find_model_name and isinstance(value, list):
                    
                    for q in value:
                        
                        try:
                            
                            json_dump = json.dumps(q)
                            validation_class.model_validate_json(json_dump)
                            
                        except ValidationError as err:
                            
                            print(err)
                            return False
                        
                        q_id: uuid.UUID = None
                        
                        if isinstance(q, dict):
                            
                            for key, value in q.items():
                                
                                if key == 'id':
                                    
                                    q_id = uuid.UUID(value)
                            
                            if q_id:
                                
                                q_get = session.get(db_class, q_id)
                                
                                if q_get:
                                    
                                    raise ValidationError
                                
                                else:
                                    
                                    try:
                                        
                                        obj = db_class.model_validate(q)
                                        
                                        obj[last_model_id_name] = last_model_id
                                        
                                        session.add(obj)

                                    except Exception as err:
                                        
                                        return False
            
            if return_model_id:
                
                return q_id
"""
class FilesController:
    
    def __init__(self):
        #files and dir
        self.main_dir = "query_folder"
        self.file_types = ['application/json']
        self.satisfied_items_root = 'satisfied_items.json'
        self.satisfied_items: dict[str, list[str]] = {}
        
        #models
        self.querys: dict[str, list[str]] = {"Query":['POST','DELETE','GET']}
        self.orders: dict[str, list[str]] = {"Order":['PATCH','GET','DELETE']}
        self.items: dict[str, list[str]] = {"Item":['PATCH','GET','DELETE']}
        
        #cur.files
        self.cur_object: str = None
        self.cur_method: str = None
        self.cur_file_data: dict = None
        
        #re patterns
        self.re_pattern = re.compile(pattern=r'Q\d{3}-\d{4}-\d{4}-\d{4}')
        
        # folder init
        if not os.path.exists(self.main_dir):
            
            os.mkdir(path=self.main_dir)
            
        os.chdir(self.main_dir)
        
        # file init //need to fix logic
        if not os.path.isfile(self.satisfied_items_root):
            
            if self.satisfied_items:
            
                for key, value in self.satisfied_items.items():
                    
                    if len(value) > 1:
                        
                        json_object = json.dumps(self.satisfied_items, indent=4)
                        
                        with open(self.satisfied_items_root,'w') as outfile:
                            
                            outfile.write(json_object)
                        
            else:
                
                start_dict = {
                    'satisfied_items': [f'{self.satisfied_items_root}']
                }
                
                json_object = json.dumps(start_dict, indent=4)
                
                with open(self.satisfied_items_root,'w') as outfile:
                    
                    outfile.write(json_object)
        
        # getting satisfied items
        try:
            
            with open(self.satisfied_items_root, 'r') as f:
                
                data = json.load(f)
                
            self.satisfied_items = data
            
        except Exception as err: # //add right exception
            
            self.__init__()
    
    # append to json file 
    def append_satisfied_item(self, file: str) -> None:
        
        for key, value in self.satisfied_items.items():
            
            value.append(file)
        
        try:
            
            json_object = json.dumps(self.satisfied_items, indent=4)
            
            with open(self.satisfied_items_root,'w') as outfile:
                
                outfile.write(json_object)
        
        except Exception as err: # //add right exception
            
            self.__init__()
    
    # file model validation
    def model_validation(self, file: str) -> bool:
        
        parameters_validation: list[bool, bool] = []
        
        try:
            
            with open(file, 'r') as f:
                
                self.cur_file_data = json.load(f)
                
            if isinstance(self.cur_file_data, dict):
                
                for name, parameter_value in self.cur_file_data.items():
                    
                    if name == 'method' and parameter_value in ['POST','PATCH','DELETE','GET']:
                        
                        self.cur_method = parameter_value
                        
                        parameters_validation.append(True)
                    
                    elif name == 'object' and parameter_value in ['Query','Item','Order','OP']:
                        
                        self.cur_object = parameter_value
                        
                        parameters_validation.append(True)
                
                if len(parameters_validation) == 2 and self.cur_method != None and self.cur_object != None:
                    
                    return True
                
                else:
                    
                    return False
                
            else:
                
                return False
                            
            
        except Exception as err: # //add right exception
            pass
        
    
    # inner file validation //can be shorter with adding logic update func
    def file_processing(self,
        file: str
        #controller = QueryesOperator(),
        ) -> bool: # add logic
        session = get_session()
            
        if self.cur_method  == 'POST' and self.cur_object == 'Query':
            
            ''' ///work in progress
            last_model_id = controller.find_query(file_data=self.cur_file_data,
            session = session, db_class = Database.QueryDB, return_model_id=True,
            is_start_func = True, validation_class = DesktopQuery)
            '''
            
            try:
                
                json_dump = json.dumps(self.cur_file_data)
                DesktopQuery.model_validate_json(json_dump) # //need to fix model validating
            
            except ValidationError as err:
                session.close()
                print(err)
                return False
            
            query_id: uuid.UUID = None
            
            # getting query id to get session 
            for key, value in self.cur_file_data.items():
                
                if key == 'id':
                    
                    query_id = uuid.UUID(value)
                    
            
            if query_id:
            
                query_get = session.get(Database.QueryDB, query_id)
                    
                if query_get:
                        
                    return False
                
                else:
                    
                    try:
                        # for query model
                        obj = Database.QueryDB.model_validate(self.cur_file_data)
                        
                        session.add(obj)
                        
                        # for orders
                        for key, value in self.cur_file_data.items():
                            
                            if key == "orders" and isinstance(value, list):
                                
                                for order in value:
                                    
                                    try:
                                        
                                        json_dump = json.dumps(order)
                                        Order.model_validate_json(json_dump)
                                    
                                    except ValidationError as err:
                                        print(err)
                                        return False

                                    order_id: uuid.UUID = None
                                    
                                    if isinstance(order, dict):
                                        
                                        for key, value in order.items():
                                            
                                            if key == 'id':
                                                
                                                order_id = uuid.UUID(value)
                                                
                                        if order_id:
                                            
                                            order_get = session.get(Database.OrderDB, order_id)
                                            
                                            if order_get:
                                                
                                                raise ValidationError #// change err type
                                            
                                            else:
                                                
                                                try:
                                                    
                                                    obj = Database.OrderDB.model_validate(order)
                                                    
                                                    obj.query_id = query_id
                                                
                                                    session.add(obj)

                                                except Exception as err:
                                                    
                                                    print(err)
                                            
                                            # for items
                                        for key, value in order.items():
                                                
                                            if key == 'items' and isinstance(value, list):
                                                
                                                for item in value:
                                                    
                                                    try:
                                        
                                                        json_dump = json.dumps(item)
                                                        Item.model_validate_json(json_dump)
                                                    
                                                    except ValidationError as err:
                                                        print(err)
                                                        return False

                                                    item_id: uuid.UUID = None
                                                    
                                                    if isinstance(item, dict):
                                        
                                                        for key, value in item.items():
                                                            
                                                            if key == 'id':
                                                                
                                                                item_id = uuid.UUID(value)
                                                                
                                                        if item_id:
                                                            
                                                            item_get = session.get(Database.ItemDB, item_id)
                                                            
                                                            if item_get:
                                                                
                                                                raise ValidationError #// change err type
                                                            
                                                            else:
                                                                
                                                                try:
                                                                    
                                                                    obj = Database.ItemDB.model_validate(item)
                                                                    
                                                                    obj.order_id = order_id
                                                                
                                                                    session.add(obj)

                                                                except Exception as err:
                                                                    
                                                                    print(err)
                                                            
                                                        for key, value in item.items():
                                                            # for op
                                                            if key == 'optional_parameters' and isinstance(value, list):
                                                                
                                                                for parameter in value:
                                                                    
                                                                    try:
                                        
                                                                        json_dump = json.dumps(parameter)
                                                                        
                                                                        OptionalParameters.model_validate_json(json_dump)
                                                                    
                                                                    except ValidationError as err:
                                                                        
                                                                        print(err)
                                                                        
                                                                        return False

                                                                    op_id: uuid.UUID = None
                                                                    
                                                                    if isinstance(parameter, dict):
                                                        
                                                                        for key, value in parameter.items():
                                                                            
                                                                            if key == 'id':
                                                                                
                                                                                op_id = uuid.UUID(value)
                                                                                
                                                                        if op_id:
                                                                            
                                                                            op_get = session.get(Database.OptionalParametersDB, op_id)
                                                                            
                                                                            if op_get:
                                                                                
                                                                                raise ValidationError #// change err type
                                                                            
                                                                            else:
                                                                                
                                                                                try:
                                                                                    
                                                                                    obj = Database.OptionalParametersDB.model_validate(parameter)
                                                                                    
                                                                                    obj.item_id = item_id
                                                                                
                                                                                    session.add(obj)

                                                                                except Exception as err:
                                                                                    
                                                                                    print(err)
                                        else:
                                            pass
                                            
                            else:
                                
                                pass            
                                            
                                        
                                        
                        
                    except Exception as e:
                        session.close()
                        print(e)
                        return False
            
            else:
                
                return False# need logic"""
        
        elif self.cur_method == 'DELETE' and self.cur_object == 'Query':
            
            try:
                
                json_dump = json.dumps(self.cur_file_data)
                DesktopQueryDelete.model_validate_json(json_dump) # // logic can be separated
            
            except ValidationError as err:
                session.close()
                print(err)
                return False
            
            query_id: uuid.UUID = None
            
            # getting query id to get session 
            for key, value in self.cur_file_data.items():
                
                if key == 'query_id':
                    
                    query_id = uuid.UUID(value)
                    
            
            if query_id:
            
                query_get = session.get(Database.QueryDB, query_id)
                    
                if query_get:
                        
                    session.delete(query_get)
                
                else:
                    
                    return False
        
        elif self.cur_method == 'DELETE' and self.cur_object == 'Order':
            
            try:
                
                json_dump = json.dumps(self.cur_file_data)
                DesktopOrderDelete.model_validate_json(json_dump) # // logic can be separated
            
            except ValidationError as err:
                session.close()
                print(err)
                return False
            
            order_id: uuid.UUID = None
            
            # getting order id to get session 
            for key, value in self.cur_file_data.items():
                
                if key == 'order_id':
                    
                    order_id = uuid.UUID(value)
                    
            
            if order_id:
            
                order_get = session.get(Database.OrderDB, order_id)
                    
                if order_get:
                        
                    session.delete(order_get)
                
                else:
                    
                    return False
        
        elif self.cur_method == 'DELETE' and self.cur_object == 'Item':
            
            try:
                
                json_dump = json.dumps(self.cur_file_data)
                DesktopItemDelete.model_validate_json(json_dump) # // logic can be separated
            
            except ValidationError as err:
                session.close()
                print(err)
                return False
            
            item_id: uuid.UUID = None
            
            # getting item id to get session 
            for key, value in self.cur_file_data.items():
                
                if key == 'item_id':
                    
                    item_id = uuid.UUID(value)
                    
            
            if item_id:
            
                item_get = session.get(Database.ItemDB, item_id)
                    
                if item_get:
                        
                    session.delete(item_get)
                
                else:
                    
                    return False
        
        elif self.cur_method == 'DELETE' and self.cur_object == 'OP':
            
            try:
                
                json_dump = json.dumps(self.cur_file_data)
                DesktopOPDelete.model_validate_json(json_dump) # // logic can be separated
            
            except ValidationError as err:
                session.close()
                print(err)
                return False
            
            op_id: uuid.UUID = None
            
            # getting itemop id to get session 
            for key, value in self.cur_file_data.items():
                
                if key == 'op_id':
                    
                    op_id = uuid.UUID(value)
                    
            
            if op_id:
            
                op_get = session.get(Database.OptionalParametersDB, op_id)
                    
                if op_get:
                        
                    session.delete(op_get)
                
                else:
                    
                    return False
        
        session.commit()
        session.close()
        return True      

        
    # file is getting validated
    def file_validation(self, file: str) -> bool:
        
        # validating file not in satisfied list
        for key, value in self.satisfied_items.items():
            
            if file in value:
                            
                return False
            
            else:
                
                pass
            
        # validating file type and name pattern is match
        file_type, file_parameter = mt.guess_type(file)
                
        if file_type in self.file_types:
            
            if file_type:
                
                for name in file.split(sep='.'):
                    
                    if self.re_pattern.match(name):
                        
                        return True
                    
                    else:
                        
                        return False
                    
            else:
                
                return False
                            
        else:
            
            return False
        
        

    def check_folder(self) -> list[str] | bool:
        
        send_files: list[str] = []
        
        for *args, files in os.walk(top=".", topdown=False):
            
            for file in files:
                
                if self.file_validation(file):

                        if self.model_validation(file):
                            
                            if self.file_processing(file):
                                
                                send_files.append(file)
                                self.append_satisfied_item(file)
                                
                            else:
                                
                                self.append_satisfied_item(file)
                        
                        else:
                            
                            self.append_satisfied_item(file)
                else:
                    
                    pass
        
        if len(send_files) > 0:
            
            return send_files

        else:
            
            return False

filecontroller = FilesController()

print(filecontroller.check_folder())