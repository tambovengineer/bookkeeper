from PySide6 import QtWidgets


class BudgetTable(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        column_headers = "Сумма Бюджет".split()
        row_headers = "День Неделя Месяц".split()

        self.setFixedHeight(100)

        self.setColumnCount(len(column_headers))
        self.setRowCount(len(row_headers))

        self.setHorizontalHeaderLabels(column_headers)
        self.setVerticalHeaderLabels(row_headers)

        self.verticalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


class BudgetWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.table_widget = BudgetTable()
        self.edit_button = QtWidgets.QPushButton("Добавить | Исправить")
        self.edit_box = QtWidgets.QLineEdit()
        self.edit_box.setPlaceholderText("0")

        self.layout.addWidget(self.table_widget, 0, 0, 1, 3)
        self.layout.addWidget(QtWidgets.QLabel("Сумма ограничения бюджета"), 1, 0)
        self.layout.addWidget(self.edit_box, 1, 1)
        self.layout.addWidget(self.edit_button, 1, 2)

    def set_data(self, data: list[str], column=1):
        for j, sums in enumerate(data):
            self.table_widget.setItem(j, column, QtWidgets.QTableWidgetItem(sums))
