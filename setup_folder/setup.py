import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QCheckBox, QStackedWidget, QFileDialog, QLineEdit, QMessageBox
)
from setup_modules.main import check_git, check_internet_connection, install_git, project_install
from setup_modules.compile import check_python_existing, install_python, create_venv, install_reqs, compile_proj

class InstallerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_folder: str = ''

    def init_ui(self):
        self.setWindowTitle("Установщик")

        self.stacked_widget = QStackedWidget()

        self.init_page_1()
        self.init_page_2()

        self.stacked_widget.setCurrentIndex(0)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.resize(500, 200)

    def init_page_1(self):
        page_1 = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("Установка системы обработки заказов")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.on_cancel)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()

        continue_button = QPushButton("Продолжить")
        continue_button.clicked.connect(self.show_page_2)
        button_layout.addWidget(continue_button)

        layout.addLayout(button_layout)
        page_1.setLayout(layout)

        self.stacked_widget.addWidget(page_1)

    def init_page_2(self):
        page_2 = QWidget()
        layout = QVBoxLayout()

        self.compile_checkbox = QCheckBox("Скомпилировать по установке")
        self.compile_checkbox.setChecked(True)
        self.test_checkbox = QCheckBox("Провести тестирование")
        self.test_checkbox.setChecked(True)
        layout.addWidget(self.compile_checkbox)
        layout.addWidget(self.test_checkbox)

        path_layout = QHBoxLayout()
        path_label = QLabel("Место для установки:")
        self.path_input = QLineEdit()
        browse_button = QPushButton("Обзор")
        browse_button.clicked.connect(self.browse_folder)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        layout.addLayout(path_layout)

        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.on_cancel)
        button_layout.addWidget(cancel_button)

        button_layout.addStretch()

        install_button = QPushButton("Установить")
        install_button.clicked.connect(self.on_install)
        button_layout.addWidget(install_button)

        layout.addLayout(button_layout)
        page_2.setLayout(layout)

        self.stacked_widget.addWidget(page_2)

    def show_page_2(self):
        self.stacked_widget.setCurrentIndex(1)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выбрать папку")
        if folder:
            self.path_input.setText(folder)

    def on_cancel(self):
        print("Установка отменена.")
        self.close()

    def on_install(self):
        
        install_path = self.path_input.text()
        
        self.current_folder = install_path

        if install_path:
            
            print(f"Установка начата. Путь: {install_path}")

            if not check_git():
                
                self.prompt_install_git()
                
            else:
                
                if project_install(install_path):
                    
                    if check_python_existing:
                        
                        if create_venv(self.current_folder):
                            
                            if install_reqs(self.current_folder):
                                
                                
                                if self.test_checkbox.checkState():
                                    pass
                                
                                if self.compile_checkbox.checkState():
                                
                                    if compile_proj(self.current_folder):
                                        
                                        pass
                            
                            
                        else:
                            
                            msg_box_err3 = QMessageBox(self)
                            msg_box_err3.setIcon(QMessageBox.Question)
                            msg_box_err3.setWindowTitle("Ошибка")
                            msg_box_err3.setText(f"Создание окружение произошло с ошибкой!")
                            msg_box_err3.exec()
                        
                    else:
                        
                        msg_box_err2 = QMessageBox(self)
                        msg_box_err2.setIcon(QMessageBox.Question)
                        msg_box_err2.setWindowTitle("Ошибка")
                        msg_box_err2.setText(f"У вас не установлен Python")
                        msg_box_err2.exec()
                        msg_box_err2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                        response = msg_box_err2.exec()
                        
                        if response == QMessageBox.Yes:
                            
                            install_python()
                            
                        else:
                            
                            QMessageBox.information(self, "Информация", "Установка отменена.")
                        
                        
                    
                else:
                    
                    msg_box_err1 = QMessageBox(self)
                    msg_box_err1.setIcon(QMessageBox.Question)
                    msg_box_err1.setWindowTitle("Ошибка")
                    msg_box_err1.setText(f"Установка завершена с ошибкой!")
                    msg_box_err1.exec()
                
        else:
            
            QMessageBox.warning(self, "Ошибка", "Путь не может быть пустым.")

    def prompt_install_git(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Git не найден")
        msg_box.setText("Git не установлен. Хотите установить его сейчас?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = msg_box.exec()

        if response == QMessageBox.Yes:
            self.install_git()
        else:
            QMessageBox.information(self, "Информация", "Установка отменена.")

    def install_git(self):
        
        if check_internet_connection():
            
            install_git()
        
        else:
            
            msg_box_err = QMessageBox(self)
            msg_box_err.setIcon(QMessageBox.Question)
            msg_box_err.setWindowTitle("Ошибка")
            msg_box_err.setText("Вы не подключены к сети!")
            msg_box_err.exec()
            
            
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstallerWindow()
    window.show()
    sys.exit(app.exec_())
