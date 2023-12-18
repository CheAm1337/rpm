#Создайте форму PyQT в соответствие с заданием:
# кнопками, элементами управления, изображения, поля ввода и др.
# Реализуйте класс в Python который позволяет выполнять основные
# математические операции (сложение, умножение, транспонирование).
# Полученные данные должны записываться в базу данных SQLite.
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

class MathOperations(QWidget):
    def __init__(self):
        super(MathOperations, self).__init__()

        # Инициализация пользовательского интерфейса
        self.init_ui()

        # Подключение к базе данных SQLite и создание таблицы
        self.db_connection = sqlite3.connect('math_operations.db')
        self.create_table()

    def init_ui(self):
        self.setWindowTitle('Math Operations')

        # Поля для ввода чисел и вывода результата
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)
        self.result_label = QLabel(self)

        # Кнопки для выполнения операций
        self.multiply_button = QPushButton('Multiply', self)
        self.addition_button = QPushButton('Addition', self)
        self.transpose_button = QPushButton('Transpose', self)
        self.save_button = QPushButton('Save and Show', self)

        # Подключение слотов
        self.multiply_button.clicked.connect(self.perform_multiplication)
        self.addition_button.clicked.connect(self.perform_addition)
        self.transpose_button.clicked.connect(self.perform_transpose)
        self.save_button.clicked.connect(self.save_and_show_result)

        # Организация интерфейса с использованием QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.input1)
        layout.addWidget(self.input2)
        layout.addWidget(self.multiply_button)
        layout.addWidget(self.addition_button)
        layout.addWidget(self.transpose_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def create_table(self):
        # Создание таблицы в базе данных для сохранения результатов
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS math_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    result TEXT NOT NULL
                )
            ''')

    def perform_multiplication(self):
        # Выполнение операции умножения
        num1 = float(self.input1.text())
        num2 = float(self.input2.text())
        result = num1 * num2

        # Отображение результата
        self.result_label.setText(f'Result (Multiplication): {result}')

    def perform_addition(self):
        # Выполнение операции сложения
        num1 = float(self.input1.text())
        num2 = float(self.input2.text())
        result = num1 + num2

        # Отображение результата
        self.result_label.setText(f'Result (Addition): {result}')

    def perform_transpose(self):
        # Выполнение операции транспонирования
        num1 = float(self.input1.text())
        num2 = float(self.input2.text())
        result = (num2, num1)

        # Отображение результата
        self.result_label.setText(f'Result (Transpose): {result}')

    def save_and_show_result(self):
        # Сохранение текущего результата в базе данных и отображение его
        current_result = self.result_label.text()

        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('INSERT INTO math_results (operation, result) VALUES (?, ?)',
                           ('Current Operation', current_result))

        # Отображение результата
        self.result_label.setText(f'Saved and Shown Result: {current_result}')


if __name__ == '__main__':
    # Запуск приложения
    app = QApplication([])
    math_operations = MathOperations()
    math_operations.show()
    app.exec_()
