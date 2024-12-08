import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt

from controllers.server_controller import ServerController
from controllers.file_controller import FileController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система обработки заказов")
        self.setGeometry(200, 200, 800, 600)
        self.setFixedSize(800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

#########################################################################
############################## MAIN_PAGE ################################
#########################################################################

        self.main_page_tab = QWidget()
        self.main_page_layout = QVBoxLayout()

        # Title: "Система обработки заказов"
        self.main_page_title = QLabel("Система обработки заказов")
        self.main_page_title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_page_title.setAlignment(Qt.AlignCenter)  # Центрирование текста

        # Subtitle: "Вас приветствует система обработки заказов"
        self.main_page_subtitle = QLabel("Вас приветствует система обработки заказов")
        self.main_page_subtitle.setStyleSheet("font-size: 18px;")
        self.main_page_subtitle.setAlignment(Qt.AlignCenter)  # Центрирование текста

        # Button: "Открыть документацию"
        self.documentation_button = QPushButton("Открыть документацию")
        self.documentation_button.setFixedSize(200, 40)  # Устанавливаем размер кнопки
        self.documentation_button.clicked.connect(self.open_documentation)  # Подключение события

        # Добавляем элементы в layout
        self.main_page_layout.addWidget(self.main_page_title)
        self.main_page_layout.addWidget(self.main_page_subtitle)
        self.main_page_layout.addWidget(self.documentation_button, alignment=Qt.AlignCenter)

        self.main_page_tab.setLayout(self.main_page_layout)
        self.tabs.addTab(self.main_page_tab, "Главная")
        
        
#########################################################################
############################ MAIN_PAGE END ##############################
#########################################################################



#########################################################################
############################## SERVER ###################################
#########################################################################

        self.server_tab = QWidget()
        self.server_layout = QVBoxLayout()
        self.server_status_label = QLabel("Сервер не запущен")
        self.server_layout.addWidget(self.server_status_label)

        self.start_server_button = QPushButton("Запустить сервер")
        self.start_server_button.clicked.connect(self.start_server)
        self.server_layout.addWidget(self.start_server_button)

        self.stop_server_button = QPushButton("Остановить сервер")
        self.stop_server_button.clicked.connect(self.stop_server)
        self.stop_server_button.setEnabled(False)  # Отключаем, пока сервер не запущен
        self.server_layout.addWidget(self.stop_server_button)

        self.server_tab.setLayout(self.server_layout)
        self.tabs.addTab(self.server_tab, "Сервер")

        # Инициализация ServerController
        self.server_controller = ServerController()
        
#########################################################################
############################ SERVER END #################################
#########################################################################


#########################################################################
########################### FILE_WORKER #################################
#########################################################################

        self.fw_tab = QWidget()
        self.fw_layout = QVBoxLayout()
        self.fw_status_label = QLabel("Сервер не запущен")
        self.fw_layout.addWidget(self.fw_status_label)

        self.start_fw_button = QPushButton("Запустить сервер")
        self.start_fw_button.clicked.connect(self.start_fw)
        self.fw_layout.addWidget(self.start_fw_button)

        self.stop_fw_button = QPushButton("Остановить сервер")
        self.stop_fw_button.clicked.connect(self.stop_fw)
        self.stop_fw_button.setEnabled(False)  # Отключаем, пока сервер не запущен
        self.fw_layout.addWidget(self.stop_fw_button)

        self.fw_tab.setLayout(self.fw_layout)
        self.tabs.addTab(self.fw_tab, "Сервер")

        # Инициализация fwController
        self.fw_controller = FileController()
        
#########################################################################
########################### FILE_WORKER END #############################
#########################################################################


#########################################################################
################################ DEFS ###################################
#########################################################################

    # main_page
    def open_documentation(self):
        # Логика для открытия документации (например, открыть URL)
        print("Открытие документации...")
        
    # server
    def start_server(self):
        self.server_controller.start_server()
        self.server_status_label.setText("Сервер запущен")
        self.start_server_button.setEnabled(False)
        self.stop_server_button.setEnabled(True)

    def stop_server(self):
        self.server_controller.close_server()
        self.server_status_label.setText("Сервер остановлен")
        self.start_server_button.setEnabled(True)
        self.stop_server_button.setEnabled(False)
    
    # file_worker
    def start_fw(self):
        self.fw_controller.start_fw()
        self.fw_status_label.setText("Обработчик файлов запущен")
        self.start_fw_button.setEnabled(False)
        self.stop_fw_button.setEnabled(True)

    def stop_fw(self):
        self.fw_controller.close_fw()
        self.fw_status_label.setText("Обработчик файлов остановлен")
        self.start_fw_button.setEnabled(True)
        self.stop_fw_button.setEnabled(False)

#########################################################################
############################# DEFS END ##################################
#########################################################################

def init_interface():
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
