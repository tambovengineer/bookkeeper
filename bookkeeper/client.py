"""Приложение для контроля финансов."""

import sys

from PySide6 import QtWidgets
from bookkeeper.presenter.presenter import Presenter


app = QtWidgets.QApplication(sys.argv)

client = Presenter()
client.window.show()
sys.exit(app.exec())
