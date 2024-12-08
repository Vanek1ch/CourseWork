from controllers.modules.server.server import Server
from controllers.main_controller import DbController
from multiprocessing import Process

import uvicorn
import multiprocessing

class ServerController:
    def __init__(self):
        self.server_process = None
        multiprocessing.freeze_support()

    @staticmethod
    def init_server():
        # Запуск FastAPI-сервера
        server_ex = Server()
        uvicorn.run(server_ex.app, host="0.0.0.0", port=8082)

    def start_server(self):
        if self.server_process is None or not self.server_process.is_alive():
            # Создаем и запускаем процесс сервера
            self.server_process = Process(name='fastapi-server-dev', target=self.init_server)
            self.server_process.daemon = True
            self.server_process.start()
            print("Сервер запущен в отдельном процессе")

    def close_server(self):
        if self.server_process and self.server_process.is_alive():
            self.server_process.terminate()
            self.server_process.join()  # Убедимся, что процесс завершен
            self.server_process = None
            print("Сервер остановлен")
