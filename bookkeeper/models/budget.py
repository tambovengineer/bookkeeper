"""Модуль бюджета"""
from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
        Класс бюджета, хранит сумму в день, неделю и месяц
        Класс используестя для хранения как ограничений бюджета,
        так и хранения суммы последних расходов.
    """
    day: float = 0
    week: float = 0
    month: float = 0
    pk: int = 0
