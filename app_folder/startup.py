from interface.interface import *
from controllers.db_controller import DbController

def init_bd():
    
    bd = DbController()
    
    bd.init_db()

def start_interface():
    
    init_bd()
    
    init_interface()

    
if __name__ == "__main__":
    
    start_interface()