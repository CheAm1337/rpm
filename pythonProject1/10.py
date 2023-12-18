#про текст

import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

class TextFileProcessor(QWidget):
    def __init__(self):
        super(TextFileProcessor, self).__init__()

        # Инициализация пользовательского интерфейса
        self.init_ui()

        # Подключение к базе данных SQLite и создание таблицы
        self.db_connection = sqlite3.connect('text_file_processor.db')
        self.create_table()

    def init_ui(self):
        self.setWindowTitle('Text File Processor')

        # Виджеты для отображения информации о текстовом файле и кнопок
        self.file_info_label = QLabel(self)
        self.open_button = QPushButton('Open Text File', self)
        self.process_button = QPushButton('Process Text File', self)
        self.save_button = QPushButton('Save File Info', self)

        # Подключение слотов
        self.open_button.clicked.connect(self.open_text_file)
        self.process_button.clicked.connect(self.process_text_file)
        self.save_button.clicked.connect(self.save_file_info)

        # Организация интерфейса с использованием QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.file_info_label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.process_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def create_table(self):
        # Создание таблицы в базе данных для сохранения результатов
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS text_file_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    extension TEXT NOT NULL,
                    char_count INTEGER NOT NULL
                )
            ''')

    def open_text_file(self):
        # Открытие текстового файла
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Text File', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                self.file_info_label.setText(f'File: {file_path}\nContent: {file_content}\nCharacter Count: {len(file_content)}')
                self.file_content = file_content

    def process_text_file(self):
        # Обработка текстового файла (в данном случае - подсчет символов)
        if hasattr(self, 'file_content'):
            char_count = len(self.file_content)
            self.file_info_label.setText(f'Content: {self.file_content}\nCharacter Count: {char_count}')

    def save_file_info(self):
        # Сохранение информации о текстовом файле в базе данных
        if hasattr(self, 'file_content'):
            filename = self.file_info_label.text().split('\n')[0].split(': ')[1]
            extension = 'txt'
            char_count = len(self.file_content)

            with self.db_connection:
                cursor = self.db_connection.cursor()
                cursor.execute('INSERT INTO text_file_info (filename, extension, char_count) VALUES (?, ?, ?)', (filename, extension, char_count))

if __name__ == '__main__':
    # Запуск приложения
    app = QApplication([])
    text_file_processor = TextFileProcessor()
    text_file_processor.show()
    app.exec_()
