from typing import List, TypedDict
from .Account import Account
from .Clock import Clock
from .FinancialEntity import FinancialEntity, NextStepData


class StockInvestmentContext(TypedDict):
    expected_yield: float
    reinvest_interval: int


class SingleInvestment(TypedDict):
    base: float
    current: float
    timestamp: int


class StockInvestment(FinancialEntity):
    def __init__(self, clock: Clock, context: StockInvestmentContext):
        super().__init__(clock)
        self.investments: List[SingleInvestment] = []
        self.context = context

    def _add_position(self, amount: float) -> None:
        self.investments.append(
            {"base": amount, "current": amount, "timestamp": self.clock.epoch}
        )

    def _sell_position(self, index: int) -> float:
        investment = self.investments.pop(index)
        current = investment["current"]
        base = investment["base"]
        revenue = current - base
        return 0.75 * revenue + base

    def deposit(self, account: Account, amount: float) -> None:
        if amount <= 0:
            raise Exception("Cannot deposit negative or zero values")
        self._add_position(amount)
        account.withdraw(amount)

    def attempt_withdrawal(self, account: Account, requested_amount: float) -> float:
        cnt = 0
        while cnt < requested_amount and len(self.investments) > 0:
            cnt += self._sell_position(0)
        if cnt > requested_amount:
            self._add_position(cnt - requested_amount)
            cnt = requested_amount
        account.deposit(cnt)
        return cnt

    def get_value(self) -> float:
        return sum([x["current"] for x in self.investments])

    def step(self) -> NextStepData:
        for investment in self.investments:
            investment["current"] = investment["current"] * (
                1 + self.context["expected_yield"]
            ) ** (1 / 12)

        for i in range(len(self.investments)):
            investment = self.investments[i]
            if (
                self.clock.epoch - investment["timestamp"]
                >= self.context["reinvest_interval"]
            ):
                self._add_position(self._sell_position(i))
                i -= 1

        return {"costs": 0}
