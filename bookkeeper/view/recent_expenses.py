from PySide6 import QtWidgets


class RecentExpensesWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        column_headers = "Дата Сумма Категория Комментарий".split()

        self.setColumnCount(len(column_headers))
        self.setRowCount(30)

        self.setHorizontalHeaderLabels(column_headers)
        self.verticalHeader().hide()

        self.horizontalHeader().setSectionResizeMode(3,  QtWidgets.QHeaderView.Stretch)

