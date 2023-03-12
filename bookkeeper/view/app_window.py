from PySide6 import QtWidgets
from bookkeeper.view.budget import BudgetWidget
from bookkeeper.view.recent_expenses import RecentExpensesWidget
from bookkeeper.view.add_expenses import AddExpensesWidget


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Bookkeeper")
        self.setFixedSize(600, 800)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QtWidgets.QLabel("Расходы"))
        self.expenses_widget = RecentExpensesWidget()
        layout.addWidget(self.expenses_widget)

        layout.addWidget(QtWidgets.QLabel("Бюджет"))
        self.budget = BudgetWidget()
        layout.addWidget(self.budget)

        self.add_expenses_widget = AddExpensesWidget()
        layout.addWidget(self.add_expenses_widget)
