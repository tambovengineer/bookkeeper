"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    added_date:   datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    comment: str = ''
    pk: int = 0
