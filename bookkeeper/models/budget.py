from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    day: float = 0
    week: float = 0
    month: float = 0
    pk: int = 0
