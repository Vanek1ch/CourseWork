from sqlmodel import select
from ..db_sqlite.models.model_forms_bd import *
from ..db_sqlite.db_interface import Database
from fastapi.encoders import jsonable_encoder
from datetime import datetime

import pandas as pd
import os 

class ExcelExport:
    
    def __init__(self, *args, **kwargs):
        
        self.queryes = None
        self.orders = None
        self.items = None
        self.ops = None
        self.main_dir = 'export'
    
    def get_session(self):
        
        controller = Database()
        
        session = controller.get_session()

        return session
        
    def get_data(self):
        
        session = self.get_session()
        
        try:
            
            self.queryes = jsonable_encoder(session.exec(select(QueryDB)).all())
            self.orders = jsonable_encoder(session.exec(select(OrderDB)).all())
            self.items = jsonable_encoder(session.exec(select(ItemDB)).all())
            self.ops = jsonable_encoder(session.exec(select(OptionalParametersDB)).all())
            
            self.dict_obj = {'queryes': self.queryes, 'orders':self.orders, 'items':self.items, 'ops': self.ops}

        except Exception as err:
            pass
        
    def write_to_excel(self,):
        
        try:
            
            if not os.path.exists(self.main_dir):
            
                os.mkdir(path=self.main_dir)
            
            os.chdir(self.main_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.name = f"export_{timestamp}.xlsx"
        
            with pd.ExcelWriter(self.name) as writer:
                
                for key, value in self.dict_obj.items():
                    
                    obj = pd.DataFrame(value)
                    
                    obj.to_excel(writer, key)
            
            return True
        
        except Exception as err:
            
            pass
        
        finally:
            
            os.chdir("..")