from multiprocessing import Process
from controllers.modules.export.out_endpoint import ExcelExport
import multiprocessing


class ExportController:
    
    def __init__(self):
        self.server_process = None
        multiprocessing.freeze_support()

    def init_export_controller(self, *args):
        try:
            export_controller = ExcelExport()
            export_controller.get_data()
            result = export_controller.write_to_excel()
            
            if result:
                print("Экспорт файлов завершен успешно")
            else:
                print("Экспорт файлов завершен с ошибкой")
        except Exception as e:
            print(f"Ошибка при выполнении экспорта: {e}")

    def start_ec(self):
        if self.server_process is None or not self.server_process.is_alive():
            self.server_process = Process(name='export controller', target=self.init_export_controller)
            self.server_process.daemon = True
            self.server_process.start()
            print("Экспорт файлов запущен в отдельном процессе")
        else:
            print("Экспорт файлов уже запущен")
