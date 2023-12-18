#Создайте форму PyQT в соответствие с заданием:
# кнопками, элементами управления, изображения, поля ввода и др.
# Реализуйте на Python класс для работы с видеофайлами.
# Полученные данные (название, продолжительность, расширение файла) должны записываться в базу данных SQLite.

import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from moviepy.editor import VideoFileClip

class VideoProcessor(QWidget):
    def __init__(self):
        super(VideoProcessor, self).__init__()

        # Инициализация пользовательского интерфейса
        self.init_ui()

        # Подключение к базе данных SQLite и создание таблицы
        self.db_connection = sqlite3.connect('video_processor.db')
        self.create_table()

    def init_ui(self):
        self.setWindowTitle('Video Processor')

        # Виджеты для отображения информации о видео и кнопок
        self.video_info_label = QLabel(self)
        self.open_button = QPushButton('Open Video File', self)
        self.process_button = QPushButton('Process Video', self)
        self.save_button = QPushButton('Save Video Info', self)

        # Подключение слотов
        self.open_button.clicked.connect(self.open_video_file)
        self.process_button.clicked.connect(self.process_video)
        self.save_button.clicked.connect(self.save_video_info)

        # Организация интерфейса с использованием QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.video_info_label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.process_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def create_table(self):
        # Создание таблицы в базе данных для сохранения результатов
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS video_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    duration INTEGER NOT NULL,
                    extension TEXT NOT NULL
                )
            ''')

    def open_video_file(self):
        # Открытие видеофайла
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Video File', '', 'Video Files (*.mp4 *.avi *.mkv)')
        if file_path:
            self.video_clip = VideoFileClip(file_path)
            self.video_info_label.setText(f'File: {file_path}')

    def process_video(self):
        # Обработка видео (в данном случае - вывод информации о видео)
        if hasattr(self, 'video_clip'):
            title = self.video_clip.filename
            duration = int(self.video_clip.duration)
            extension = self.video_clip.fps

            info_text = f'Title: {title}\nDuration: {duration} seconds\nFPS: {extension}'
            self.video_info_label.setText(info_text)

    def save_video_info(self):
        # Сохранение информации о видео в базе данных
        if hasattr(self, 'video_clip'):
            title = self.video_clip.filename
            duration = int(self.video_clip.duration)
            fps = self.video_clip.fps

            with self.db_connection:
                cursor = self.db_connection.cursor()
                cursor.execute('INSERT INTO video_info (title, duration, fps) VALUES (?, ?, ?)', (title, duration, fps))


if __name__ == '__main__':
    # Запуск приложения
    app = QApplication([])
    video_processor = VideoProcessor()
    video_processor.show()
    app.exec_()
