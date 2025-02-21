from typing import TypedDict
from .Clock import Clock
from .FinancialEntity import FinancialEntity


class OtherCostsOfLivingContext(TypedDict):
    initial_costs: float
    yearly_inflation: float


class OtherCostsOfLiving(FinancialEntity):
    def __init__(self, clock: Clock, context: OtherCostsOfLivingContext):
        super().__init__(clock)
        self.context = context
        self.costs = context["initial_costs"]

    def get_costs(self) -> float:
        return self.costs

    def get_value(self) -> float:
        return 0

    def onTick(self):
        super().onTick()
        self.costs = self.costs * (1 + self.context["yearly_inflation"]) ** (1 / 12)
