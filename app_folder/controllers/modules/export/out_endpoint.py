from modules.db_sqlite.db_interface import *
from sqlmodel import Session, select
from modules.db_sqlite.models.model_forms import *
from modules.db_sqlite.db_interface import *
from fastapi.encoders import jsonable_encoder
import pandas as pd

Controller = Database()
Controller.init_db() # later to delete because of server

engine = Controller.return_engine()

# func to get session
def get_session():
    session = Session(engine)
    return session

class ExcelExport:
    
    def __init__(self, *args, **kwargs):
        
        self.queryes = None
        self.orders = None
        self.items = None
        self.ops = None
    
    def get_data(self,):
        
        session = get_session()
        
        try:
            
            self.queryes = jsonable_encoder(session.exec(select(Database.QueryDB)).all())
            self.orders = jsonable_encoder(session.exec(select(Database.OrderDB)).all())
            self.items = jsonable_encoder(session.exec(select(Database.ItemDB)).all())
            self.ops = jsonable_encoder(session.exec(select(Database.OptionalParametersDB)).all())
            
            self.dict_obj = {'queryes': self.queryes, 'orders':self.orders, 'items':self.items, 'ops': self.ops}

        except Exception as err:
            pass
        
    def write_to_excel(self,):
        
        try:
        
            with pd.ExcelWriter('outfile.xlsx') as writer:
                
                for key, value in self.dict_obj.items():
                    
                    obj = pd.DataFrame(value)
                    
                    obj.to_excel(writer, key)
        
        except Exception as err:
            pass
        
excelout = ExcelExport()
excelout.get_data()
excelout.write_to_excel()
