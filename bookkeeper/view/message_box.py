"""Модуль диалогового окна"""
from PySide6 import QtWidgets


class MessageBox(QtWidgets.QMessageBox):
    """Класс диалогового окна"""
    def __init__(self,
                 window_title: str = 'window',
                 message: str = 'message',
                 is_critical: bool = False,
                 add_cancel: bool = False) -> None:
        super().__init__()

        self.setWindowTitle(window_title)
        self.setText(message)

        if add_cancel:
            self.button_flag = QtWidgets.QMessageBox.StandardButton.Ok \
                               | QtWidgets.QMessageBox.StandardButton.Cancel
        else:
            self.button_flag = QtWidgets.QMessageBox.StandardButton.Ok
        self.setStandardButtons(self.button_flag)

        if is_critical:
            self.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        else:
            self.setIcon(QtWidgets.QMessageBox.Icon.Information)
