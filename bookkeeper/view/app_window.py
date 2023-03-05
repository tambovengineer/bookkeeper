import sys

from PySide6 import QtWidgets
from bookkeeper.view.budget import BudgetWidget
from bookkeeper.view.recent_expenses import RecentExpensesWidget


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Bookkeeper")
        #self.setFixedSize(600, 600)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QtWidgets.QLabel("Расходы"))
        self.expenses_widget = RecentExpensesWidget()
        self.layout.addWidget(self.expenses_widget)

        self.layout.addWidget(QtWidgets.QLabel("Бюджет"))
        self.budget = BudgetWidget()
        self.layout.addWidget(self.budget)
        self.layout.addWidget(QtWidgets.QLabel("Бюджет"))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
