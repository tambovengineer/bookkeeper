"""Модуль виджета таблицы бюджета"""
from PySide6 import QtWidgets


class BudgetTable(QtWidgets.QTableWidget):
    """Класс виджета таблицы бюджета"""
    def __init__(self) -> None:
        super().__init__()

        self.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        column_headers = "Сумма Бюджет".split()
        row_headers = "День Неделя Месяц".split()

        self.setFixedHeight(100)

        self.setColumnCount(len(column_headers))
        self.setRowCount(len(row_headers))

        self.setHorizontalHeaderLabels(column_headers)
        self.setVerticalHeaderLabels(row_headers)

        self.verticalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)


class BudgetWidget(QtWidgets.QWidget):
    """Класс виджета интерфейса бюджета расходов"""
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        self.table_widget = BudgetTable()
        self.edit_button = QtWidgets.QPushButton("Добавить | Исправить")
        self.edit_box = QtWidgets.QLineEdit()
        self.edit_box.setPlaceholderText("0")

        layout.addWidget(self.table_widget, 0, 0, 1, 3)
        layout.addWidget(QtWidgets.QLabel("Сумма ограничения бюджета"), 1, 0)
        layout.addWidget(self.edit_box, 1, 1)
        layout.addWidget(self.edit_button, 1, 2)

    def set_data(self, data: list[str], column: int = 1) -> None:
        """Функция для записи данных в таблицу"""
        for j, sums in enumerate(data):
            self.table_widget.setItem(j, column, QtWidgets.QTableWidgetItem(sums))
