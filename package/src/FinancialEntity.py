from __future__ import annotations
from typing import Any, TypedDict
from .Clock import Clock


class NextStepData(TypedDict):
    costs: float


class FinancialEntity:
    def __init__(self, clock: Clock):
        self.clock = clock
        # We generally start with no costs as there aren't any costs upon
        # obtaining a valued entity. Costs only occur after the first time span.
        self.costs_to_pay = 0
        clock.listen(self.onTick)

    def step(self) -> NextStepData:
        raise NotImplementedError

    # account is actually of type Account here, but to avoid circular references
    # it is typed as Any.
    def pay_costs(self, account: Any) -> None:
        if self.costs_to_pay == 0:
            return
        account.withdraw(self.costs_to_pay)
        self.costs_to_pay = 0

    def get_value(self) -> float:
        raise NotImplementedError

    def onTick(self) -> None:
        if self.costs_to_pay > 0:
            raise Exception("Costs have not been paid yet!")
        data = self.step()
        self.costs_to_pay = data["costs"]
