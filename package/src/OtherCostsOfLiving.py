from typing import TypedDict
from .Clock import Clock
from .FinancialEntity import FinancialEntity, NextStepData


class OtherCostsOfLivingContext(TypedDict):
    initial_costs: float
    yearly_inflation: float


class OtherCostsOfLiving(FinancialEntity):
    def __init__(self, clock: Clock, context: OtherCostsOfLivingContext):
        super().__init__(clock)
        self.context = context
        self.monthly_costs = context["initial_costs"]

    def get_value(self) -> float:
        return 0

    def step(self) -> NextStepData:
        self.monthly_costs = self.monthly_costs * (
            1 + self.context["yearly_inflation"]
        ) ** (1 / 12)
        return {"costs": self.monthly_costs}
