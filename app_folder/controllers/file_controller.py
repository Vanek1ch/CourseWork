from time import sleep
from multiprocessing import Process
from controllers.modules.file_processing.file_worker import FilesController
import multiprocessing

class FileController:
    
    def __init__(self):
        self.server_process = None
        multiprocessing.freeze_support()

    def init_file_controller(*args):
        
        file_controller = FilesController()

        while True:
            
            files = file_controller.check_folder()
            
            if files:
                
                print('Find files: ', len(files))
                
            else:
                
                print('Searching for files...')
                
                sleep(15)
        
    def start_fw(self):
        if self.server_process is None or not self.server_process.is_alive():
            self.server_process = Process(name='file-controller', target=self.init_file_controller)
            self.server_process.daemon = True
            self.server_process.start()
            print("Обработчик файлов запущен в отдельном процессе")

    def close_fw(self):
        if self.server_process and self.server_process.is_alive():
            self.server_process.terminate()
            self.server_process.join()
            self.server_process = None
            print("Обработчик файлов завершил работу")