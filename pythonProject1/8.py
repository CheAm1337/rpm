#Создайте форму PyQT в соответствие с заданием:
# кнопками, элементами управления, изображения, поля ввода и др.
# Реализуйте на Python класс для работы с аудиофайлами.
# Полученные данные (исполнитель, название трека, время) должны записываться в базу данных SQLite
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from pydub import AudioSegment

class AudioProcessor(QWidget):
    def __init__(self):
        super(AudioProcessor, self).__init__()

        # Инициализация пользовательского интерфейса
        self.init_ui()

        # Подключение к базе данных SQLite и создание таблицы
        self.db_connection = sqlite3.connect('audio_processor.db')
        self.create_table()

    def init_ui(self):
        self.setWindowTitle('Audio Processor')

        # Виджеты для отображения информации о треке и кнопок
        self.track_info_label = QLabel(self)
        self.open_button = QPushButton('Open Audio File', self)
        self.process_button = QPushButton('Process Audio', self)
        self.save_button = QPushButton('Save Track Info', self)

        # Подключение слотов
        self.open_button.clicked.connect(self.open_audio_file)
        self.process_button.clicked.connect(self.process_audio)
        self.save_button.clicked.connect(self.save_track_info)

        # Организация интерфейса с использованием QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.track_info_label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.process_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def create_table(self):
        # Создание таблицы в базе данных для сохранения результатов
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audio_track_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    artist TEXT NOT NULL,
                    title TEXT NOT NULL,
                    duration INTEGER NOT NULL
                )
            ''')

    def open_audio_file(self):
        # Открытие аудиофайла
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Audio File', '',
                                                   'Audio Files (*.mp3 *.wav *.ogg *.flac)')
        if file_path:
            try:
                # Проверка расширения файла и выбор соответствующего формата для pydub
                _, extension = os.path.splitext(file_path)
                extension = extension.lower()
                audio_formats = {'.mp3': 'mp3', '.wav': 'wav', '.ogg': 'ogg', '.flac': 'flac'}

                if extension in audio_formats:
                    self.audio = AudioSegment.from_file(file_path, format=audio_formats[extension])
                    self.track_info_label.setText(f'File: {file_path}')
                else:
                    raise ValueError(f'Unsupported audio format: {extension}')

            except Exception as e:
                # Обработка возможных ошибок при открытии аудиофайла
                print(f"Error opening audio file: {e}")

    def process_audio(self):
        # Обработка аудио (в данном случае - вывод информации о треке)
        if hasattr(self, 'audio'):
            artist = self.audio.tags.get('artist', 'Unknown Artist')
            title = self.audio.tags.get('title', 'Unknown Title')
            duration = len(self.audio) // 1000  # Продолжительность в секундах

            info_text = f'Artist: {artist}\nTitle: {title}\nDuration: {duration} seconds'
            self.track_info_label.setText(info_text)

    def save_track_info(self):
        # Сохранение информации о треке в базе данных
        if hasattr(self, 'audio'):
            artist = self.audio.tags.get('artist', 'Unknown Artist')
            title = self.audio.tags.get('title', 'Unknown Title')
            duration = len(self.audio) // 1000  # Продолжительность в секундах

            with self.db_connection:
                cursor = self.db_connection.cursor()
                cursor.execute('INSERT INTO audio_track_info (artist, title, duration) VALUES (?, ?, ?)', (artist, title, duration))

if __name__ == '__main__':
    # Запуск приложения
    app = QApplication([])
    audio_processor = AudioProcessor()
    audio_processor.show()
    app.exec_()
