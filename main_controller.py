from db_interface import Database
from server import Server
from interface import *
from file_worker import *
from multiprocessing import Process
from time import sleep
import uvicorn

def start_server(db_path):
    controller = Database()
    engine = controller.return_engine()
    server_ex = Server(engine=engine)
    uvicorn.run(server_ex.app, host="0.0.0.0", port=8082)

def start_file_controller(db_path):
    controller = Database()
    engine = controller.return_engine()
    file_controller = FilesController(engine=engine, db_controller=controller)

    while True:
        files = file_controller.check_folder()
        if files:
            print('Find files: ', len(files))
        else:
            print('Searching for files...')
            sleep(15)


def start_interface():
    webview.start()



def start_all():
    controller = Database()
    controller.init_db()
    db_path = "database.db"

    server_process = Process(name='fastapi-server-dev', target=start_server, args=(db_path,))
    file_controller_process = Process(name='file_controller', target=start_file_controller, args=(db_path,))
    interface_process = Process(name='interface', target=start_interface)

    server_process.start()
    file_controller_process.start()
    interface_process.start()

    server_process.join()
    file_controller_process.join()
    interface_process.join()



if __name__ == '__main__':
    start_all()
