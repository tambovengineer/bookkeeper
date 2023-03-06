from PySide6 import QtWidgets
from bookkeeper.view.edit_categories import EditCategoriesWidget


class AddExpensesWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QtWidgets.QLabel("Сумма"), 0, 0)
        self.layout.addWidget(QtWidgets.QLabel("Категория"), 1, 0)

        self.edit_box = QtWidgets.QLineEdit()
        self.edit_box.setPlaceholderText("0")

        self.categories_list = ["Продукты", "Книги", "Транспорт"]
        self.categories_list_widget = QtWidgets.QComboBox()
        self.categories_list_widget.addItems(self.categories_list)

        self.add_button = QtWidgets.QPushButton("Добавить")

        self.edit_button = QtWidgets.QPushButton("Редактировать")
        self.edit_button.clicked.connect(self.edit_button_click)

        self.layout.addWidget(self.edit_box, 0, 1)
        self.layout.addWidget(self.categories_list_widget, 1, 1)
        self.layout.addWidget(self.add_button, 2, 1)
        self.layout.addWidget(self.edit_button, 1, 2)

    def edit_button_click(self):
        EditCategoriesWidget(self.categories_list).exec()
        self.categories_list_widget.clear()
        self.categories_list_widget.addItems(self.categories_list)
