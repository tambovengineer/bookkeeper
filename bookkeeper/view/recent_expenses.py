from PySide6 import QtWidgets
from bookkeeper.models.expense import Expense


class RecentExpensesWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        column_headers = "Дата Сумма Категория Комментарий".split()

        self.setColumnCount(len(column_headers))
        # self.setRowCount(30)
        self.setFixedHeight(300)

        self.setHorizontalHeaderLabels(column_headers)
        self.verticalHeader().hide()

        self.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def set_data(self, data: list[Expense]):
        self.setRowCount(0)
        self.setRowCount(len(data))

        for i, expense in enumerate(data):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(
                expense.expense_date))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(expense.amount)))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(str(expense.category)))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(expense.comment))



