"""Модуль виджета редактирования категорий и записей о расходах"""
from PySide6 import QtWidgets, QtCore


class AddExpensesWidget(QtWidgets.QWidget):
    """Класс виджета таблицы бюджета"""
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QtWidgets.QLabel("Сумма"), 0, 0)
        layout.addWidget(QtWidgets.QLabel("Комментарий"), 1, 0)
        layout.addWidget(QtWidgets.QLabel("Категория"), 2, 0)
        layout.addWidget(QtWidgets.QLabel("Дата"), 3, 0)
        layout.addWidget(QtWidgets.QLabel("Название новой категории"), 5, 0)

        self.edit_box = QtWidgets.QLineEdit()
        self.edit_box.setPlaceholderText("0")

        self.edit_comment_box = QtWidgets.QLineEdit()
        self.edit_comment_box.setPlaceholderText("Комментарий")

        self.categories_list = ["Продукты", "Книги", "Транспорт"]
        self.categories_list_widget = QtWidgets.QComboBox()
        self.categories_list_widget.addItems(self.categories_list)

        self.add_button = QtWidgets.QPushButton("Добавить запись")
        self.edit_expense_button = QtWidgets.QPushButton("Исправить запись")
        self.del_button = QtWidgets.QPushButton("Удалить запись")

        self.add_comment_button = QtWidgets.QPushButton("Добавить категорию")
        self.edit_comment_button = QtWidgets.QPushButton("Исправить категорию")
        self.del_comment_button = QtWidgets.QPushButton("Удалить категорию")

        self.help_button = QtWidgets.QPushButton("Справка...")
        self.help_button.setDefault(True)

        self.edit_category_box = QtWidgets.QLineEdit()
        self.edit_category_box.setPlaceholderText("Разное")

        self.edit_date = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())

        layout.addWidget(self.edit_box, 0, 1, 1, 3)
        layout.addWidget(self.edit_comment_box, 1, 1, 1, 3)
        layout.addWidget(self.categories_list_widget, 2, 1, 1, 3)
        layout.addWidget(self.add_button, 4, 1)
        layout.addWidget(self.edit_expense_button, 4, 2)
        layout.addWidget(self.del_button, 4, 3)
        layout.addWidget(self.edit_category_box, 5, 1, 1, 3)
        layout.addWidget(self.add_comment_button, 6, 1)
        layout.addWidget(self.edit_comment_button, 6, 2)
        layout.addWidget(self.del_comment_button, 6, 3)
        layout.addWidget(self.edit_date, 3, 1, 1, 3)

        layout.addWidget(self.help_button, 7, 3)
