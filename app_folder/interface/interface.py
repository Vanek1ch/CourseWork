import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QLineEdit, QTabWidget, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt

from controllers.server_controller import ServerController
from controllers.file_controller import FileController
from controllers.export_controller import ExportController
from interface.inf_bd_controller import Database, create_user, login_user

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система обработки заказов")
        self.setGeometry(200, 200, 800, 600)
        self.setFixedSize(800, 600)
        
        self.user_role: str = None

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_login_page()
        self.create_registration_page()
        self.tabs.setCurrentWidget(self.login_tab)
        
#########################################################################
############################ LOGIN PAGE #################################
#########################################################################

    def create_login_page(self):
        self.login_tab = QWidget()
        self.login_layout = QVBoxLayout()

        # Заголовок: "Вход в аккаунт"
        self.login_title = QLabel("Вход в аккаунт")
        self.login_title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.login_title.setAlignment(Qt.AlignCenter)

        # Поле ввода логина
        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите ваш логин")

        # Поле ввода пароля
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.setFixedSize(200, 40)
        self.login_button.clicked.connect(self.login)

        # Кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setFixedSize(200, 40)
        self.register_button.clicked.connect(self.open_registration_page)

        # Добавляем элементы в layout
        self.login_layout.addWidget(self.login_title)
        self.login_layout.addWidget(self.login_label)
        self.login_layout.addWidget(self.login_input)
        self.login_layout.addWidget(self.password_label)
        self.login_layout.addWidget(self.password_input)
        self.login_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        self.login_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        self.login_tab.setLayout(self.login_layout)
        self.tabs.addTab(self.login_tab, "Вход")

#########################################################################
########################## REGISTRATION PAGE ###########################
#########################################################################

    def create_registration_page(self):
        self.registration_tab = QWidget()
        self.registration_layout = QVBoxLayout()

        # Заголовок: "Регистрация"
        self.registration_title = QLabel("Регистрация")
        self.registration_title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.registration_title.setAlignment(Qt.AlignCenter)

        # Поле ввода логина
        self.new_login_label = QLabel("Логин:")
        self.new_login_input = QLineEdit()
        self.new_login_input.setPlaceholderText("Введите логин")

        # Поле ввода пароля
        self.new_password_label = QLabel("Пароль:")
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Введите пароль")
        self.new_password_input.setEchoMode(QLineEdit.Password)

        # Кнопка регистрации
        self.create_account_button = QPushButton("Создать аккаунт")
        self.create_account_button.setFixedSize(200, 40)
        self.create_account_button.clicked.connect(self.register)

        # Кнопка возврата к входу
        self.back_to_login_button = QPushButton("Назад к входу")
        self.back_to_login_button.setFixedSize(200, 40)
        self.back_to_login_button.clicked.connect(self.open_login_page)

        # Добавляем элементы в layout
        self.registration_layout.addWidget(self.registration_title)
        self.registration_layout.addWidget(self.new_login_label)
        self.registration_layout.addWidget(self.new_login_input)
        self.registration_layout.addWidget(self.new_password_label)
        self.registration_layout.addWidget(self.new_password_input)
        self.registration_layout.addWidget(self.create_account_button, alignment=Qt.AlignCenter)
        self.registration_layout.addWidget(self.back_to_login_button, alignment=Qt.AlignCenter)

        self.registration_tab.setLayout(self.registration_layout)
        self.tabs.addTab(self.registration_tab, "Регистрация")

#########################################################################
############################ LOGIN/REGISTRATION #########################
#########################################################################

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        if login and password:
            
            key, *args = login_user(name=login, password=password).items()
            
            if not key:
                
                QMessageBox.warning(self, "Ошибка", args)
            
            else:
                
                QMessageBox.warning(self, "Успех!", "Вы успешно вошли!")
                
                self.user_role = args
            
        else:
            
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")

    def register(self):
        new_login = self.new_login_input.text()
        new_password = self.new_password_input.text()

        if new_login and new_password:
            
            if create_user(name = new_login, password = new_password):
            
                QMessageBox.warning(self, "Успех", "Пользователь создан верно!")
                
            else:
                QMessageBox.warning(self, "Ошибка", "Данный пользователь уже существует!")
        else:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")

    def open_login_page(self):
        self.tabs.setCurrentWidget(self.login_tab)

    def open_registration_page(self):
        self.tabs.setCurrentWidget(self.registration_tab)
        
    def separator(self):
        pass


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
        self.server_status_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.server_status_label.setAlignment(Qt.AlignCenter)  # Центрирование текста
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
        self.fw_status_label = QLabel("Обработчик файлов не запущен")
        self.fw_status_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.fw_status_label.setAlignment(Qt.AlignCenter)  # Центрирование текста
        self.fw_layout.addWidget(self.fw_status_label)

        self.start_fw_button = QPushButton("Запустить обработчик файлов")
        self.start_fw_button.clicked.connect(self.start_fw)
        self.fw_layout.addWidget(self.start_fw_button)

        self.stop_fw_button = QPushButton("Остановить обработчик файлов")
        self.stop_fw_button.clicked.connect(self.stop_fw)
        self.stop_fw_button.setEnabled(False)  # Отключаем, пока сервер не запущен
        self.fw_layout.addWidget(self.stop_fw_button)

        self.fw_tab.setLayout(self.fw_layout)
        self.tabs.addTab(self.fw_tab, "Обработчик файлов")

        # Инициализация fwController
        self.fw_controller = FileController()
        
#########################################################################
########################### FILE_WORKER END #############################
#########################################################################

#########################################################################
############################## EXPORT ###################################
#########################################################################

        self.export_tab = QWidget()
        self.export_layout = QVBoxLayout()
        self.export_status_label = QLabel("Экспортировать в excel")
        self.export_status_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.export_status_label.setAlignment(Qt.AlignCenter)  # Центрирование текста
        self.export_layout.addWidget(self.export_status_label)

        self.start_export_button = QPushButton("Экспорт в Excel")
        self.start_export_button.clicked.connect(self.start_export)
        self.export_layout.addWidget(self.start_export_button)

        self.export_tab.setLayout(self.export_layout)
        self.tabs.addTab(self.export_tab, "Экспорт файлов")

        # Инициализация ExportController
        self.export_controller = ExportController()
        
#########################################################################
############################ EXPORT END #################################
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
        
    # export
    def start_export(self):
        self.export_controller.start_ec()

#########################################################################
############################# DEFS END ##################################
#########################################################################

def init_interface():
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
