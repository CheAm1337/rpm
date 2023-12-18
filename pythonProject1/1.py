#Создайте форму PyQT в соответствие с заданием:
# кнопками, элементами управления, изображения, поля ввода и др.
# Приложения для ввода основной информации о человеке (фамилия, имя, возраст, группа),
# данные должны сохранятся в базе данных SQLite.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3

# Создаем экземпляр QApplication (приложения)
app = QApplication(sys.argv)

# Создаем главное окно приложения
window = QWidget()
window.setWindowTitle('Ввод информации о человеке')

# Создаем виджеты для ввода данных
label_lastname = QLabel('Фамилия:')
edit_lastname = QLineEdit()

label_firstname = QLabel('Имя:')
edit_firstname = QLineEdit()

label_age = QLabel('Возраст:')
edit_age = QLineEdit()

label_group = QLabel('Группа:')
edit_group = QLineEdit()

# Кнопка для сохранения данных
save_button = QPushButton('Сохранить')

# Создаем основной макет окна
layout = QVBoxLayout()

# Макет для размещения полей ввода
form_layout = QVBoxLayout()
form_layout.addWidget(label_lastname)
form_layout.addWidget(edit_lastname)
form_layout.addWidget(label_firstname)
form_layout.addWidget(edit_firstname)
form_layout.addWidget(label_age)
form_layout.addWidget(edit_age)
form_layout.addWidget(label_group)
form_layout.addWidget(edit_group)

# Макет для размещения кнопки сохранения
button_layout = QVBoxLayout()
button_layout.addWidget(save_button)

# Добавляем созданные макеты в основной макет
layout.addLayout(form_layout)
layout.addLayout(button_layout)

# Устанавливаем основной макет для главного окна
window.setLayout(layout)

# Функция для сохранения данных в базе
def save_data():
    lastname = edit_lastname.text()
    firstname = edit_firstname.text()
    age = edit_age.text()
    group = edit_group.text()

    # Проверяем, что все поля ввода заполнены
    if lastname and firstname and age and group:
        # Подключаемся к базе данных SQLite
        connection = sqlite3.connect('people.db')
        cursor = connection.cursor()

        # Создаем таблицу people, если её еще нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS people
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lastname TEXT,
                           firstname TEXT,
                           age INTEGER,
                           group_name TEXT)''')

        # Вставляем данные в таблицу people
        cursor.execute('INSERT INTO people (lastname, firstname, age, group_name) VALUES (?, ?, ?, ?)',
                       (lastname, firstname, int(age), group))

        # Фиксируем изменения и закрываем соединение с базой данных
        connection.commit()
        connection.close()

        # Выводим сообщение об успешном сохранении данных
        QMessageBox.information(window, 'Сохранение данных', 'Данные успешно сохранены в базе данных.')

# Подключаем функцию сохранения данных к событию нажатия кнопки
save_button.clicked.connect(save_data)

# Отображаем главное окно
window.show()

# Запускаем цикл обработки событий приложения
sys.exit(app.exec_())
