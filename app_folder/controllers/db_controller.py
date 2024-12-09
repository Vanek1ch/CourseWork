from controllers.modules.db_sqlite.db_interface import Database

class DbController():
    
    def __init__(self):
        
        self.db = Database('database.db')
        
    
    def init_db(self):
        self.db.init_db()
    
    def return_class(self):
        return self.db
    
    def return_engine(self):
        engine = self.db.engine
        return engine
        
'''from db_sqlite.db_interface import Database
from server.server import Server
from interface.interface import *
from file_processing.file_worker import *
from multiprocessing import Process
from time import sleep
import uvicorn
#
#
#   ###      #####    ######    #####      #####    ######        #        #######    #####    ###                    
#   #   #    #        #    #    #    #     #        #            # #          #       #        #   #
#   #   #    #####    ######    #####      #####    #           #   #         #       #####    #   #            
#   #   #    #        #         #   #      #        #          #######        #       #        #   #
#   ###      #####    #         #     #    #####    ######    #       #       #       #####    ###              
#
#
# Функция для инициализации базы данных
def initialize_database(db_path):
    controller = Database(db_path=db_path)
    controller.init_db()


# Запуск FastAPI сервера
def start_server(db_path):
    controller = Database(db_path=db_path)
    engine = controller.return_engine()
    server_ex = Server(engine=engine)
    uvicorn.run(server_ex.app, host="0.0.0.0", port=8082)


# Запуск обработки файлов
def start_file_controller(db_path):
    controller = Database(db_path=db_path)
    engine = controller.return_engine()
    file_controller = FilesController(engine=engine, db_controller=controller)

    while True:
        files = file_controller.check_folder()
        if files:
            print('Find files: ', len(files))
        else:
            print('Searching for files...')
            sleep(15)


# Основная функция для запуска всех процессов
def start_all():
    db_path = "database.db"

    # Инициализация базы данных
    initialize_database(db_path)

    # Создание процессов
    server_process = Process(name='fastapi-server-dev', target=start_server, args=(db_path,))
    file_controller_process = Process(name='file_controller', target=start_file_controller, args=(db_path,))

    # Запуск процессов
    server_process.start()
    file_controller_process.start()

    # Ожидание завершения процессов
    server_process.join()
    file_controller_process.join()
'''