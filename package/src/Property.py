from typing import TypedDict
from .Account import Account
from .Clock import Clock
from .FinancialEntity import FinancialEntity


class PropertyContext(TypedDict):
    area: float
    price_per_square_meter: float
    monthly_rent_per_square_meter: float
    yearly_value_increase_percentage: float
    yearly_maintenance_costs_percentage: float
    property_purchase_tax_rate: float
    property_purchase_notary_cost_rate: float
    property_purchase_brokerage: float


class Property(FinancialEntity):
    def __init__(self, clock: Clock, context: PropertyContext):
        super().__init__(clock)
        self.context: PropertyContext = context
        self.value: float = context["area"] * context["price_per_square_meter"]
        self.monthly_rent: float = (
            context["area"] * context["monthly_rent_per_square_meter"]
        )
        self.owned: bool = False

    def get_total_purchase_costs(self) -> float:
        tax_rate = self.context["property_purchase_tax_rate"]
        notary_costs_rate = self.context["property_purchase_notary_cost_rate"]
        brokerage = self.context["property_purchase_brokerage"]
        return self.value * (1 + tax_rate + notary_costs_rate + brokerage)

    def buy(self, account: Account):
        account.withdraw(self.get_total_purchase_costs())
        self.owned = True

    def get_costs(self) -> float:
        if self.costs_paid:
            return 0
        if self.owned:
            maintenance_costs = (
                self.value * self.context["yearly_maintenance_costs_percentage"] / 12
            )
            return maintenance_costs
        else:
            return self.monthly_rent

    def get_value(self) -> float:
        return self.value if self.owned else 0

    def onTick(self):
        super().onTick()
        inc = self.context["yearly_value_increase_percentage"]
        self.value = self.value * (1 + inc) ** (1 / 12)
        self.monthly_rent = self.monthly_rent * (1 + inc) ** (1 / 12)
