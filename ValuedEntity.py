from __future__ import annotations
from typing import Any
from Clock import Clock


class ValuedEntity:
    def __init__(self, clock: Clock):
        self.clock = clock
        # We generally start with costs being paid as there aren't any costs upon
        # obtaining a valued entity. Costs only occur after the first time span.
        self.costs_paid = True
        clock.listen(self.onTick)

    def get_costs(self) -> float:
        raise NotImplementedError

    # account is actually of type Account here, but to avoid circular references
    # it is typed as Any.
    def pay_costs(self, account: Any) -> None:
        if self.costs_paid:
            return
        account.withdraw(self.get_costs())
        self.costs_paid = True

    def get_value(self) -> float:
        raise NotImplementedError

    def onTick(self) -> None:
        if not self.costs_paid:
            raise Exception("Costs have not been paid yet!")
        self.costs_paid = False
