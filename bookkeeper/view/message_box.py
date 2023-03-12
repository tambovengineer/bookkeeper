from PySide6 import QtWidgets


class MessageBox(QtWidgets.QMessageBox):
    def __init__(self,
                 window_title='window',
                 message='message',
                 is_critical=False,
                 add_cancel=False) -> None:
        super().__init__()

        self.setWindowTitle(window_title)
        self.setText(message)

        if add_cancel:
            self.button_flag = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        else:
            self.button_flag = QtWidgets.QMessageBox.Ok
        self.setStandardButtons(self.button_flag)

        if is_critical:
            self.setIcon(QtWidgets.QMessageBox.Critical)
        else:
            self.setIcon(QtWidgets.QMessageBox.Information)
