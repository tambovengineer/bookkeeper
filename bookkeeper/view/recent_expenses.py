from PySide6 import QtWidgets


class RecentExpensesWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        column_headers = "Дата Сумма Категория Комментарий".split()

        self.setColumnCount(len(column_headers))
        self.setFixedHeight(300)

        self.setHorizontalHeaderLabels(column_headers)
        self.verticalHeader().hide()

        self.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def set_data(self, data: list[list[str]]) -> None:
        self.setRowCount(0)
        self.setRowCount(len(data))

        for i, expense in enumerate(data):
            for j, expense_str in enumerate(expense):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(expense_str))
