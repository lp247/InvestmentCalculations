from __future__ import annotations
from .Clock import Clock
from .FinancialEntity import FinancialEntity


class Account(FinancialEntity):
    def __init__(self, clock: Clock, initial: float):
        super().__init__(clock)
        self.balance = initial

    def deposit(self, amount: float):
        self.balance += amount

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise Exception(
                "Cannot withdraw more than is available: Available "
                + str(self.balance)
                + ", Requested: "
                + str(amount)
            )
        self.balance -= amount

    def get_costs(self) -> float:
        return 0

    def get_value(self) -> float:
        return self.balance

    def onTick(self) -> None:
        super().onTick()
