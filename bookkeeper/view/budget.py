from PySide6 import QtWidgets


class BudgetWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

