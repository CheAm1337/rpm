#Создайте форму PyQT в соответствие с заданием:
# кнопками, элементами управления, изображения, поля ввода и др.
# Разработайте класс для работы с файлами в Python, который позволяет
# копировать, перемещать и удалять файлы, а также создавать директории.
# Добавьте базу данных SQLite для записи созданных директорий. Приложение должно выполнять команды ОС Linux.
import os
import shutil
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog

class FileManager(QWidget):
    def __init__(self):
        super(FileManager, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('File Manager')

        # Кнопки для различных операций с файлами и директориями
        self.create_dir_button = QPushButton('Create Directory')
        self.create_dir_button.clicked.connect(self.create_directory)

        self.copy_button = QPushButton('Copy File')
        self.copy_button.clicked.connect(self.copy_file)

        self.move_button = QPushButton('Move File')
        self.move_button.clicked.connect(self.move_file)

        self.delete_button = QPushButton('Delete File/Directory')
        self.delete_button.clicked.connect(self.delete_file)

        # Подключение к базе данных SQLite и создание таблицы
        self.db_connection = sqlite3.connect('file_manager.db')
        self.create_table()

        # Организация интерфейса с использованием QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.create_dir_button)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.move_button)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def create_table(self):
        # Создание таблицы в базе данных для отслеживания директорий
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS directories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL
                )
            ''')

    def create_directory(self):
        # Создание директории и запись в базу данных
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            os.makedirs(dir_path)
            if os.path.isdir(dir_path):
                self.insert_directory_to_db(dir_path)

    def copy_file(self):
        # Копирование файла
        src_file, _ = QFileDialog.getOpenFileName(self, 'Select File to Copy')
        if src_file:
            dest_file, _ = QFileDialog.getSaveFileName(self, 'Select Destination for Copy')
            if dest_file:
                shutil.copy(src_file, dest_file)

    def move_file(self):
        # Перемещение файла
        src_file, _ = QFileDialog.getOpenFileName(self, 'Select File to Move')
        if src_file:
            dest_file, _ = QFileDialog.getSaveFileName(self, 'Select Destination for Move')
            if dest_file:
                shutil.move(src_file, dest_file)

    def delete_file(self):
        # Удаление файла или директории
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File/Directory to Delete')
        if file_path:
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                self.remove_directory_from_db(file_path)

    def insert_directory_to_db(self, path):
        # Вставка записи о директории в базу данных
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('INSERT INTO directories (path) VALUES (?)', (path,))

    def remove_directory_from_db(self, path):
        # Удаление записи о директории из базы данных
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('DELETE FROM directories WHERE path = ?', (path,))

if __name__ == '__main__':
    # Запуск приложения
    app = QApplication([])
    file_manager = FileManager()
    file_manager.show()
    app.exec_()
