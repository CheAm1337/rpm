import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
import sqlite3

class MyApp(QWidget):
    def __init__(self, db_name):
        super().__init__()

        # Инициализация приложения
        self.db_name = db_name
        self.init_ui()

    def init_ui(self):
        # Настройка интерфейса приложения
        self.setWindowTitle('Пример PyQt с SQLite')
        self.setGeometry(100, 100, 600, 400)

        # Инициализация базы данных
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Создание таблицы 'users' при необходимости
        table_name = 'users'
        columns = ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'name TEXT', 'age INTEGER']
        self.create_table(table_name, columns)

        # Виджеты
        self.name_label = QLabel('Имя:')
        self.name_entry = QLineEdit()

        self.age_label = QLabel('Возраст:')
        self.age_entry = QLineEdit()

        self.add_button = QPushButton('Добавить в базу данных')
        self.add_button.clicked.connect(self.add_to_database)

        self.query_button = QPushButton('Выполнить запрос')
        self.query_button.clicked.connect(self.execute_query)

        self.result_label = QLabel('Результат запроса:')
        self.result_table = QTableWidget()

        # Расположение виджетов на форме
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_entry)
        form_layout.addWidget(self.age_label)
        form_layout.addWidget(self.age_entry)
        form_layout.addWidget(self.add_button)
        form_layout.addWidget(self.query_button)
        form_layout.addWidget(self.result_label)
        form_layout.addWidget(self.result_table)

        self.setLayout(form_layout)

    def create_table(self, table_name, columns):
        # Создание таблицы в базе данных
        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def add_to_database(self):
        # Добавление записи в базу данных
        name = self.name_entry.text()
        age = self.age_entry.text()

        if name and age:
            user_data = (None, name, int(age))  # None для автоматического присвоения уникального id
            self.insert_data('users', user_data)
            self.name_entry.clear()
            self.age_entry.clear()

    def insert_data(self, table_name, data):
        # Вставка данных в таблицу
        placeholders = ', '.join(['?' for _ in range(len(data))])
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def execute_query(self):
        # Выполнение SQL-запроса
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        self.result_table.setRowCount(len(result))
        self.result_table.setColumnCount(len(result[0]) if result else 0)

        for i, row in enumerate(result):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                self.result_table.setItem(i, j, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp('example.db')
    window.show()
    sys.exit(app.exec_())
