from PySide6 import QtWidgets, QtCore


class EditCategoriesWidget(QtWidgets.QDialog):
    def __init__(self, categories_list, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Изменение категорий")

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QtWidgets.QLabel("Категория для удаления"))
        #self.categories_list = ["Продукты", "Книги", "Транспорт"]
        self.categories_list = categories_list
        self.categories_list_widget = QtWidgets.QComboBox()
        self.categories_list_widget.addItems(self.categories_list)
        self.layout.addWidget(self.categories_list_widget)
        self.delete_button = QtWidgets.QPushButton("Удалить")
        self.layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_click)

        self.layout.addWidget(QtWidgets.QLabel("Название категории для добавления"))
        self.edit_box = QtWidgets.QLineEdit()
        self.edit_box.setPlaceholderText("Название")
        self.layout.addWidget(self.edit_box)
        self.add_button = QtWidgets.QPushButton("Добавить")
        self.layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_click)

        # self.button_layout = QtWidgets.QHBoxLayout()
        # self.button_layout.addWidget(QtWidgets.QPushButton("Добавить"))
        # self.button_layout.addWidget(QtWidgets.QPushButton("Удалить"))
        # self.layout.addLayout(self.button_layout)

    def delete_click(self):
        # self.categories_list.remove(self.categories_list_widget.currentText())
        if self.categories_list_widget.count() == 1:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText('В списке категорий должен присутствовать хотя бы один элемент.')
            msgBox.setWindowTitle("Ошибка")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()

            return


        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText('Вы действительно хотите удалить категорию? Действие нельзя отменить.')
        msgBox.setWindowTitle("Удаление категории")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        ret = msgBox.exec()

        if ret == QtWidgets.QMessageBox.Ok:
            self.categories_list_widget.removeItem(self.categories_list_widget.currentIndex())
            self.categories_list.pop(self.categories_list_widget.currentIndex())

    def add_click(self):
        txt = self.edit_box.text()

        if txt == "":
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText('Поле "Название" пустое.')
            msgBox.setWindowTitle("Ошибка")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()

            return
        elif self.categories_list_widget.findText(txt) != -1:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText('Введенная категория уже есть в списке.')
            msgBox.setWindowTitle("Ошибка")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()

            return

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText('Категория добавлена.')
        msgBox.setWindowTitle("Добавление категории")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()

        self.categories_list_widget.addItem(self.edit_box.text())
        self.categories_list.append(self.edit_box.text())
