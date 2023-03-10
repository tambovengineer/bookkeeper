import sys

from PySide6 import QtWidgets
from bookkeeper.view.app_window import MainWindow
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.view.message_box import MessageBox
from bookkeeper.utils import read_tree


class Client:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()

        self.exp_rep = MemoryRepository[Expense]()

        self.window.expenses_widget.set_data(self.exp_rep.get_all())

        self.window.add_expenses_widget.del_button.clicked.connect(self.del_handler)
        self.window.add_expenses_widget.add_button.clicked.connect(self.add_handler)
        self.window.add_expenses_widget.edit_expense_button.clicked.connect(self.edit_handler)

    def del_handler(self):
        if self.window.expenses_widget.rowCount() == 0:
            msg = MessageBox('Ошибка', 'Список пуст.', is_critical=True, add_cancel=False).exec()
            return

        if self.window.expenses_widget.currentRow() == -1:
            msg = MessageBox('Ошибка', 'Выберите строку для удаления.', is_critical=True, add_cancel=False).exec()
            return

        msg = MessageBox('Удаление записи',
                         'Вы действительно хотите удалить выбранную запись?',
                         is_critical=False,
                         add_cancel=True).exec()

        if msg == QtWidgets.QMessageBox.Cancel:
            return

        row_num = self.window.expenses_widget.currentRow()
        del_pk = self.exp_rep.get_all()[row_num].pk

        self.exp_rep.delete(del_pk)
        self.window.expenses_widget.set_data(self.exp_rep.get_all())

    def add_handler(self):
        amount_txt = self.window.add_expenses_widget.edit_box.text()

        try:
            amount = float(amount_txt)
        except ValueError:
            msg = MessageBox('Ошибка',
                             'Сумма должна быть числом.',
                             is_critical=True, add_cancel=False).exec()
            return

        if amount <= 0:
            msg = MessageBox('Ошибка',
                             'Сумма должна быть положительной.',
                             is_critical=True, add_cancel=False).exec()
            return

        comment = self.window.add_expenses_widget.edit_comment_box.text()

        new_exp = Expense(amount=amount,
                          category=self.window.add_expenses_widget.categories_list_widget.currentText(),
                          comment=comment)
        self.exp_rep.add(new_exp)
        self.window.expenses_widget.set_data(self.exp_rep.get_all())

        # msg = MessageBox('Добавление записи', 'Запись добавлена.', is_critical=False, add_cancel=False).exec()

    def edit_handler(self):
        if self.window.expenses_widget.rowCount() == 0:
            msg = MessageBox('Ошибка', 'Список пуст.', is_critical=True, add_cancel=False).exec()
            return

        if self.window.expenses_widget.currentRow() == -1:
            msg = MessageBox('Ошибка', 'Выберите строку для исправления.', is_critical=True, add_cancel=False).exec()
            return

        amount_txt = self.window.add_expenses_widget.edit_box.text()

        try:
            amount = float(amount_txt)
        except ValueError:
            msg = MessageBox('Ошибка',
                             'Сумма должна быть числом.',
                             is_critical=True, add_cancel=False).exec()
            return

        if amount <= 0:
            msg = MessageBox('Ошибка',
                             'Сумма должна быть положительной.',
                             is_critical=True, add_cancel=False).exec()
            return

        msg = MessageBox('Удаление записи',
                         'Вы действительно хотите изменить выбранную запись?',
                         is_critical=False,
                         add_cancel=True).exec()

        comment = self.window.add_expenses_widget.edit_comment_box.text()

        if msg == QtWidgets.QMessageBox.Cancel:
            return

        row_num = self.window.expenses_widget.currentRow()
        edit_pk = self.exp_rep.get_all()[row_num].pk

        new_exp = Expense(pk=edit_pk,
                          amount=amount,
                          category=self.window.add_expenses_widget.categories_list_widget.currentText(),
                          comment=comment)

        self.exp_rep.update(new_exp)
        self.window.expenses_widget.set_data(self.exp_rep.get_all())


client = Client()
client.window.show()
client.app.exec()
