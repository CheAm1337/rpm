#Создайте форму PyQT в соответствие с заданием:
# кнопками, элементами управления, изображения, поля ввода и др.
# Реализуйте на Python класс для работы с изображениями,
# позволяющий открывать, изменять размер, сохранять.
# Полученные данные должны записываться в базу данных SQLite.


import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QInputDialog
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFileDialog
from PIL import Image, ImageQt

class ImageProcessor(QWidget):
    def __init__(self):
        super(ImageProcessor, self).__init__()

        # Инициализация пользовательского интерфейса
        self.init_ui()

        # Подключение к базе данных SQLite и создание таблицы
        self.db_connection = sqlite3.connect('image_processor.db')
        self.create_table()

    def init_ui(self):
        self.setWindowTitle('Image Processor')

        # Виджеты для отображения изображения и кнопок
        self.image_label = QLabel(self)
        self.open_button = QPushButton('Open Image', self)
        self.resize_button = QPushButton('Resize Image', self)
        self.save_button = QPushButton('Save Image', self)

        # Подключение слотов
        self.open_button.clicked.connect(self.open_image)
        self.resize_button.clicked.connect(self.resize_image)
        self.save_button.clicked.connect(self.save_image)

        # Организация интерфейса с использованием QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.resize_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def create_table(self):
        # Создание таблицы в базе данных для сохранения результатов
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS image_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    result BLOB NOT NULL
                )
            ''')

    def open_image(self):
        # Открытие изображения
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)')
        if file_path:
            image = Image.open(file_path)
            self.show_image(image)

    def show_image(self, image):
        # Отображение изображения в QLabel
        q_image = ImageQt.ImageQt(image)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def resize_image(self):
        # Изменение размера изображения
        if not self.image_label.pixmap():
            return

        new_width, ok = QInputDialog.getInt(self, 'Resize Image', 'Enter new width:')
        if ok:
            pixmap = self.image_label.pixmap()
            resized_pixmap = pixmap.scaledToWidth(new_width)
            self.image_label.setPixmap(resized_pixmap)

    def save_image(self):
        # Сохранение изображения в базе данных
        if not self.image_label.pixmap():
            return

        image = self.image_label.pixmap().toImage()
        image_bytes = QByteArray()
        buffer = QBuffer(image_bytes)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, 'PNG')

        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('INSERT INTO image_results (operation, result) VALUES (?, ?)', ('Save Image', image_bytes))

if __name__ == '__main__':
    # Запуск приложения
    app = QApplication([])
    image_processor = ImageProcessor()
    image_processor.show()
    app.exec_()
