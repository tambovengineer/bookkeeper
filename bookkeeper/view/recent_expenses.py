"""Модуль виджета таблицы расходов"""
from PySide6 import QtWidgets


class RecentExpensesWidget(QtWidgets.QTableWidget):
    """Класс виджета таблицы расходов"""
    def __init__(self) -> None:
        super().__init__()

        self.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        column_headers = "Дата Сумма Категория Комментарий".split()

        self.setColumnCount(len(column_headers))
        self.setFixedHeight(300)

        self.setHorizontalHeaderLabels(column_headers)
        self.verticalHeader().hide()

        self.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def set_data(self, data: list[list[str]]) -> None:
        """Функция для записи данных в таблицу"""
        self.setRowCount(0)
        self.setRowCount(len(data))

        for i, expense in enumerate(data):
            for j, expense_str in enumerate(expense):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(expense_str))
