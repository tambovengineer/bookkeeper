"""Модуль описывает класс Presenter приложения"""

import sys

from PySide6 import QtWidgets
from bookkeeper.presenter.presenter import Presenter


app = QtWidgets.QApplication(sys.argv)

client = Presenter()
client.window.show()
app.exec()
