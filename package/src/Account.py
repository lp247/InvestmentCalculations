from __future__ import annotations
from typing import TypedDict
from .Clock import Clock
from .FinancialEntity import FinancialEntity, NextStepData


class AccountContext(TypedDict):
    initial_cash: float
    overdraft_loan_rate: float


class Account(FinancialEntity):
    def __init__(self, clock: Clock, context: AccountContext):
        super().__init__(clock)
        self.context = context
        self.balance = context["initial_cash"]

    def deposit(self, amount: float):
        self.balance += amount

    def withdraw(self, amount: float):
        self.balance -= amount

    def get_value(self) -> float:
        return self.balance

    def step(self) -> NextStepData:
        if self.balance < 0:
            overdraft_loan_rate = self.context["overdraft_loan_rate"]
            self.balance = self.balance * (1 + overdraft_loan_rate) ** (1 / 12)
        return {"costs": 0}
