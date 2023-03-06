from PySide6 import QtWidgets


class RecentExpensesTable(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        column_headers = "Дата Сумма Категория Комментарий".split()

        self.setColumnCount(len(column_headers))
        self.setRowCount(30)

        self.setHorizontalHeaderLabels(column_headers)
        self.verticalHeader().hide()

        self.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)


class RecentExpensesWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.expenses_table = RecentExpensesTable()

        self.layout.addWidget(self.expenses_table)

        self.del_button = QtWidgets.QPushButton("Удалить запись")

        self.layout.addWidget(self.del_button)

        self.del_button.clicked.connect(self.del_expense)

        self.set_data([["2023", "10", "Конфеты", "Комментарий"],
                       ["2022", "10", "Конфеты", "Комментарий"],
                       ["2021", "10", "Конфеты", "Комментарий"],
                       ["2020", "10", "Конфеты", "Комментарий"],
                       ["2019", "10", "Конфеты", "Комментарий"],
                       ["2018", "10", "Конфеты", "Комментарий"],
                       ["2017", "10", "Конфеты", "Комментарий"]])

    def del_expense(self):
        self.expenses_table.removeRow(
            self.expenses_table.currentRow()
        )

    def set_data(self, data):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.expenses_table.setItem(
                    i, j, QtWidgets.QTableWidgetItem(x)
                )
