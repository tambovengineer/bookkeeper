from PySide6 import QtWidgets


class EditCategoriesWidget(QtWidgets.QDialog):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Изменение категорий")

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QtWidgets.QLabel("Категория для удаления"))
        self.categories_list = ["Продукты", "Книги", "Транспорт"]
        self.categories_list_widget = QtWidgets.QComboBox()
        self.categories_list_widget.addItems(self.categories_list)
        self.layout.addWidget(self.categories_list_widget)
        self.layout.addWidget(QtWidgets.QPushButton("Удалить"))

        self.layout.addWidget(QtWidgets.QLabel("Название категории дял добавления"))
        self.edit_box = QtWidgets.QLineEdit()
        self.edit_box.setPlaceholderText("Название")
        self.layout.addWidget(self.edit_box)
        self.layout.addWidget(QtWidgets.QPushButton("Добавить"))

        # self.button_layout = QtWidgets.QHBoxLayout()
        # self.button_layout.addWidget(QtWidgets.QPushButton("Добавить"))
        # self.button_layout.addWidget(QtWidgets.QPushButton("Удалить"))
        # self.layout.addLayout(self.button_layout)
