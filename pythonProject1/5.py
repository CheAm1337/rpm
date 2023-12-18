#Создайте форму PyQT в соответствие с заданием:
# кнопками, элементами управления, изображения, поля ввода и др.
# Разработайте класс в Python для работы с датами и временем,
# который позволяет выполнять различные операции, такие как вычисление
# разницы между двумя датами. Полученные данные должны сохраняться в базе данных SQLite.


import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QDateTimeEdit
from PyQt5.QtCore import Qt

class DateTimeManager(QWidget):
    def __init__(self):
        super(DateTimeManager, self).__init__()

        # Инициализация пользовательского интерфейса
        self.init_ui()

        # Подключение к базе данных SQLite и создание таблицы
        self.db_connection = sqlite3.connect('datetime_manager.db')
        self.create_table()

    def init_ui(self):
        self.setWindowTitle('Date and Time Manager')

        # Виджеты для ввода дат и вывода результатов
        self.date_time_edit1 = QDateTimeEdit(self)
        self.date_time_edit2 = QDateTimeEdit(self)
        self.date_time_edit2.setDateTime(self.date_time_edit1.dateTime())  # Установка второго виджета на текущую дату и время
        self.result_label = QLabel(self)

        # Кнопка для вычисления разницы между датами
        self.calculate_button = QPushButton('Calculate Difference', self)
        self.calculate_button.clicked.connect(self.calculate_difference)

        # Организация интерфейса с использованием QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.date_time_edit1)
        layout.addWidget(self.date_time_edit2)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def create_table(self):
        # Создание таблицы в базе данных для сохранения результатов
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS time_difference (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    result TEXT NOT NULL
                )
            ''')

    def calculate_difference(self):
        # Вычисление разницы между датами
        date_time1 = self.date_time_edit1.dateTime().toPyDateTime()
        date_time2 = self.date_time_edit2.dateTime().toPyDateTime()

        difference = date_time2 - date_time1

        # Отображение разницы в секундах
        result_text = f'Difference: {difference.total_seconds()} seconds'

        # Вывод результата на экран и сохранение в базе данных
        self.result_label.setText(result_text)
        self.save_result_to_db(result_text)

    def save_result_to_db(self, result):
        # Сохранение результата в базе данных
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('INSERT INTO time_difference (result) VALUES (?)', (result,))

if __name__ == '__main__':
    # Запуск приложения
    app = QApplication([])
    date_time_manager = DateTimeManager()
    date_time_manager.show()
    app.exec_()
