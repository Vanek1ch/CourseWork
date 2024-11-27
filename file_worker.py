import os
import json
import mimetypes as mt
import re
from sqlmodel import Session, select
from fastapi import Depends
from typing import Annotated
from db_interface import Database

#Controller = Database()
#Controller.init_db() # later to delete because of server

#engine = Controller.return_engine() 

# func to get session
#def get_session():
#    with Session(engine) as session:
#        yield session         

class FilesController():
    
    def __init__(self):
        
        self.main_dir = "query_folder"
        self.file_types = ['application/json']
        self.satisfied_items_root = 'satisfied_items.json'
        self.satisfied_items: dict[str, list[str]] = {}
        
        self.querys: dict[str, list[str]] = {"Query":['POST','DELETE','GET']}
        self.orders: dict[str, list[str]] = {"Order":['PATCH','GET','DELETE']}
        self.items: dict[str, list[str]] = {"Item":['PATCH','GET','DELETE']}
        
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
    
    def model_validation(self, file: str) -> bool:
        try:
            
            with open(file, 'r') as f:
                
                file_data = json.load(f)
            
            print(file_data)
                
            
            
        except Exception as err: # //add right exception
            pass
        
    # file is getting validated
    def file_validation(self, file: str) -> bool:
        
        # validating file not in satisfied lis
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
        
        send_files = []
        
        for *args, files in os.walk(top=".", topdown=False):
            
            for file in files:
                
                if self.file_validation(file):

                        if self.model_validation(file):
                            
                            send_files.append(file)
                            
                            self.append_satisfied_item(file)
                        
                        else:
                            pass
                else:
                    
                    pass
                
        if len(send_files) > 0:
            
            return send_files
        
        else: 
            
            return False

filecontroller = FilesController()

print(filecontroller.check_folder())