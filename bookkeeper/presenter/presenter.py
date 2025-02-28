"""Модуль описывает класс Presenter приложения"""

from datetime import datetime, timedelta, time

from PySide6 import QtWidgets, QtGui
from bookkeeper.view.app_window import MainWindow
# from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.view.message_box import MessageBox


class Presenter:
    """Класс Presenter приложения"""

    def __init__(self) -> None:
        self.window = MainWindow()

        # self.exp_rep = MemoryRepository[Expense]()
        self.exp_rep: SQLiteRepository[Expense] = SQLiteRepository(
            db_file="mem.db", cls=Expense)
        self.cat_rep: SQLiteRepository[Category] = SQLiteRepository(
            db_file="mem.db", cls=Category)
        self.budget_rep: SQLiteRepository[Budget] = SQLiteRepository(
            db_file="mem.db", cls=Budget)

        if self.cat_rep.get_all() is None:
            self.cat_rep.add(Category('Разное', None))

        if self.budget_rep.get_all() is None:
            self.budget_rep.add(Budget())

        budget = self.budget_rep.get(pk=1)

        self.window.budget.set_data([str(budget.day),
                                     str(budget.week),
                                     str(budget.month)])

        self.window.expenses_widget.set_data(self.exp_to_list())
        self.window.add_expenses_widget.categories_list_widget.clear()
        self.window.add_expenses_widget.categories_list_widget \
            .insertItems(0, self.cat_to_list())

        self.window.add_expenses_widget.del_button.\
            clicked.connect(self.del_handler)  # type: ignore[attr-defined]
        self.window.add_expenses_widget.add_button.\
            clicked.connect(self.add_handler)  # type: ignore[attr-defined]
        self.window.add_expenses_widget.edit_expense_button \
            .clicked.connect(self.edit_handler)  # type: ignore[attr-defined]

        self.window.add_expenses_widget.del_comment_button \
            .clicked.connect(self.delete_cat_handler)  # type: ignore[attr-defined]
        self.window.add_expenses_widget.add_comment_button \
            .clicked.connect(self.add_cat_handler)  # type: ignore[attr-defined]
        self.window.add_expenses_widget.edit_comment_button \
            .clicked.connect(self.edit_cat_handler)  # type: ignore[attr-defined]

        self.window.add_expenses_widget.help_button.\
            clicked.connect(self.help_handler)  # type: ignore[attr-defined]

        self.window.budget.edit_button.\
            clicked.connect(self.edit_budget)  # type: ignore[attr-defined]

        self.window.budget.edit_button.\
            clicked.connect(self.calc_budget)  # type: ignore[attr-defined]

        self.calc_budget()

    def cat_to_list(self) -> list[str]:
        """Получение из репозитория списка категорий для виджета"""
        res = []
        cat_list = self.cat_rep.get_all()

        if cat_list is not None:
            for cat in cat_list:
                res.append(cat.name)

        return res

    def exp_to_list(self) -> list[list[str]]:
        """Получение из репозитория таблицы расходов для виджета"""
        res = []
        expenses = self.exp_rep.get_all()
        if expenses is not None:
            for exp_class in expenses:
                name = self.cat_rep.get(exp_class.category).name

                res.append([exp_class.expense_date,
                            str(exp_class.amount),
                            name,
                            exp_class.comment])

        return res

    def del_handler(self) -> None:
        """Обработчик кнопки удаления записи"""

        if self.window.expenses_widget.rowCount() == 0:
            MessageBox('Ошибка', 'Список пуст.',
                       is_critical=True, add_cancel=False).exec()
            return

        if self.window.expenses_widget.currentRow() == -1:
            MessageBox('Ошибка', 'Выберите строку для удаления.',
                       is_critical=True, add_cancel=False).exec()
            return

        msg = MessageBox('Удаление записи',
                         'Вы действительно хотите удалить выбранную запись?',
                         is_critical=False, add_cancel=True).exec()

        if msg == QtWidgets.QMessageBox.StandardButton.Cancel:
            return

        row_num = self.window.expenses_widget.currentRow()
        del_pk = self.exp_rep.get_all()[row_num].pk

        self.exp_rep.delete(del_pk)
        self.window.expenses_widget.set_data(self.exp_to_list())

        self.calc_budget()

    def add_handler(self) -> None:
        """Обработчик кнопки добавления записи"""

        amount_txt = self.window.add_expenses_widget.edit_box.text()

        try:
            amount = float(amount_txt)
        except ValueError:
            MessageBox('Ошибка',
                       'Сумма должна быть числом.',
                       is_critical=True, add_cancel=False).exec()
            return

        if amount <= 0:
            MessageBox('Ошибка',
                       'Сумма должна быть положительной.',
                       is_critical=True, add_cancel=False).exec()
            return

        comment = self.window.add_expenses_widget.edit_comment_box.text()

        date = self.window.add_expenses_widget.edit_date\
            .dateTime().toPython().strftime("%m/%d/%Y, %H:%M:%S")

        num = self.window.add_expenses_widget.categories_list_widget.currentIndex()

        cat_pk = self.cat_rep.get_all()[num].pk

        new_exp = Expense(amount=amount,
                          category=cat_pk,
                          comment=comment,
                          expense_date=date)
        self.exp_rep.add(new_exp)
        self.window.expenses_widget.set_data(self.exp_to_list())

        MessageBox('Добавление записи', 'Запись добавлена.',
                   is_critical=False, add_cancel=False).exec()

        self.calc_budget()

    def edit_handler(self) -> None:
        """Обработчик кнопки редактирования записи"""

        if self.window.expenses_widget.rowCount() == 0:
            MessageBox('Ошибка', 'Список пуст.',
                       is_critical=True, add_cancel=False).exec()
            return

        if self.window.expenses_widget.currentRow() == -1:
            MessageBox('Ошибка', 'Выберите строку для исправления.',
                       is_critical=True, add_cancel=False).exec()
            return

        amount_txt = self.window.add_expenses_widget.edit_box.text()

        try:
            amount = float(amount_txt)
        except ValueError:
            MessageBox('Ошибка',
                       'Сумма должна быть числом.',
                       is_critical=True, add_cancel=False).exec()
            return

        if amount <= 0:
            MessageBox('Ошибка',
                       'Сумма должна быть положительной.',
                       is_critical=True, add_cancel=False).exec()
            return

        msg = MessageBox('Изменение записи',
                         'Вы действительно хотите изменить выбранную запись?',
                         is_critical=False,
                         add_cancel=True).exec()

        comment = self.window.add_expenses_widget.edit_comment_box.text()

        if msg == QtWidgets.QMessageBox.StandardButton.Cancel:
            return

        row_num = self.window.expenses_widget.currentRow()
        edit_pk = self.exp_rep.get_all()[row_num].pk

        date = self.window.add_expenses_widget.edit_date\
            .dateTime().toPython().strftime("%m/%d/%Y, %H:%M:%S")

        num = self.window.add_expenses_widget.categories_list_widget.currentIndex()

        cat_pk = self.cat_rep.get_all()[num].pk

        new_exp = Expense(pk=edit_pk,
                          amount=amount,
                          category=cat_pk,
                          expense_date=date,
                          comment=comment)

        self.exp_rep.update(new_exp)
        self.window.expenses_widget.set_data(self.exp_to_list())

        self.calc_budget()

    def help_handler(self) -> None:
        """Обработчик кнопки вызова справки"""

        help_text = "Программа ведения расходов.\n" \
                    "Для изменения / удаления записи" \
                    " или органичения бюджета выберите ее в таблице.\n"

        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Справка")
        dialog.setText(help_text)

        dialog.exec()

    def add_cat_handler(self) -> None:
        """Обработчик кнопки добавления категории"""

        txt = self.window.add_expenses_widget.edit_category_box.text()

        if txt == "":
            MessageBox('Ошибка', 'Поле новой категории пустое.',
                       is_critical=True, add_cancel=False).exec()
            return

        if self.window.add_expenses_widget.categories_list_widget.findText(txt) != -1:
            MessageBox('Ошибка', 'Введенная категория уже есть в списке.',
                       is_critical=True, add_cancel=False).exec()
            return

        self.cat_rep.add(Category(txt, None))

        self.window.add_expenses_widget.categories_list_widget.clear()
        self.window.add_expenses_widget.categories_list_widget \
            .insertItems(0, self.cat_to_list())

    def edit_cat_handler(self) -> None:
        """Обработчик кнопки редактирования категории"""

        txt = self.window.add_expenses_widget.edit_category_box.text()

        if txt == "":
            MessageBox('Ошибка', 'Поле новой категории пустое.',
                       is_critical=True, add_cancel=False).exec()
            return

        if self.window.add_expenses_widget.categories_list_widget.findText(txt) != -1:
            MessageBox('Ошибка', 'Введенная категория уже есть в списке.',
                       is_critical=True, add_cancel=False).exec()
            return

        num = self.window.add_expenses_widget.categories_list_widget.currentIndex()
        edit_pk = self.cat_rep.get_all()[num].pk

        new_cat = Category(txt, None)
        new_cat.pk = edit_pk
        self.cat_rep.update(new_cat)

        self.window.add_expenses_widget.categories_list_widget \
            .clear()
        self.window.add_expenses_widget.categories_list_widget \
            .insertItems(0, self.cat_to_list())

        self.window.expenses_widget.set_data(self.exp_to_list())

    def delete_cat_handler(self) -> None:
        """Обработчик кнопки удаления категории"""

        if self.window.add_expenses_widget.categories_list_widget.count() == 1:
            MessageBox('Ошибка',
                       'В списке категорий должен присутствовать хотя бы один элемент.',
                       is_critical=True, add_cancel=False).exec()
            return

        msg = MessageBox('Удаление записи',
                         'Вы действительно хотите удалить выбранную категорию?',
                         is_critical=False,
                         add_cancel=True).exec()

        if msg == QtWidgets.QMessageBox.StandardButton.Cancel:
            return

        num = self.window.add_expenses_widget.categories_list_widget.currentIndex()
        del_pk = self.cat_rep.get_all()[num].pk

        self.cat_rep.delete(del_pk)

        self.window.add_expenses_widget.categories_list_widget \
            .clear()
        self.window.add_expenses_widget.categories_list_widget \
            .insertItems(0, self.cat_to_list())

        exp_list = self.exp_rep.get_all()  # REDO !!!

        for expense in exp_list:
            if expense.category == del_pk:
                self.exp_rep.delete(expense.pk)

        self.window.expenses_widget.set_data(self.exp_to_list())

        self.calc_budget()

    def edit_budget(self) -> None:
        """Обработчик кнопки редактирования ограничения бюджета"""

        row_num = self.window.budget.table_widget.currentRow()

        enter_sum = self.window.budget.edit_box.text()

        if row_num == -1:
            MessageBox('Ошибка', 'Выберите строку для исправления.',
                       is_critical=True, add_cancel=False).exec()
            return

        try:
            amount = float(enter_sum)
        except ValueError:
            MessageBox('Ошибка',
                       'Сумма должна быть числом.',
                       is_critical=True, add_cancel=False).exec()
            return

        if amount <= 0:
            MessageBox('Ошибка',
                       'Сумма должна быть положительной.',
                       is_critical=True, add_cancel=False).exec()
            return

        MessageBox('Изменение записи',
                   'Вы действительно хотите изменить выбранную запись?',
                   is_critical=False,
                   add_cancel=True).exec()

        budget = self.budget_rep.get(pk=1)

        if row_num == 0:
            budget.day = amount
        elif row_num == 1:
            budget.week = amount
        elif row_num == 2:
            budget.month = amount

        self.budget_rep.update(budget)

        self.window.budget.set_data([str(budget.day),
                                     str(budget.week),
                                     str(budget.month)], column=1)

        self.calc_budget()

    def calc_budget(self) -> None:
        """Функция перерасчета бюджета"""

        res = Budget()

        current_date = datetime.now()
        exp_data = self.exp_rep.get_all()

        if exp_data is not None:
            for expense in exp_data:
                exp_date = datetime.strptime(expense.expense_date, "%m/%d/%Y, %H:%M:%S")

                if exp_date.date() == current_date.date():
                    res.day = res.day + expense.amount

                if datetime.combine(current_date, time.min) \
                        - timedelta(days=current_date.weekday()) <= exp_date:
                    res.week = res.week + expense.amount

                if exp_date.month == current_date.month \
                        and exp_date.year == current_date.year:
                    res.month = res.month + expense.amount

        self.window.budget.set_data([str(res.day),
                                     str(res.week),
                                     str(res.month)], column=0)

        if res.day > self.budget_rep.get(pk=1).day:
            self.window.budget.table_widget.item(0, 1) \
                .setBackground(QtGui.QColor(255, 0, 0))
        else:
            self.window.budget.table_widget.item(0, 1) \
                .setBackground(QtGui.QColor(255, 255, 255))

        if res.week > self.budget_rep.get(pk=1).week:
            self.window.budget.table_widget.item(1, 1) \
                .setBackground(QtGui.QColor(255, 0, 0))
        else:
            self.window.budget.table_widget.item(1, 1) \
                .setBackground(QtGui.QColor(255, 255, 255))

        if res.month > self.budget_rep.get(pk=1).month:
            self.window.budget.table_widget.item(2, 1) \
                .setBackground(QtGui.QColor(255, 0, 0))
        else:
            self.window.budget.table_widget.item(2, 1) \
                .setBackground(QtGui.QColor(255, 255, 255))
