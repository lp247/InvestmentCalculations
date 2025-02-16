from Account import Account
from Clock import TimeVariant
from Financing import Financing
from config import (
    PROPERTY_VALUE_INCREASE_PER_YEAR,
    RENT_PER_SQUARE_METER,
    PRICE_PER_SQUARE_METER,
    YEARLY_PROPERTY_MAINTENANCE_COSTS,
)


class Property(TimeVariant):
    def __init__(self, clock, area: int):
        super().__init__(clock)
        self._value = area * PRICE_PER_SQUARE_METER
        self._rent = area * RENT_PER_SQUARE_METER
        self._owned = False
        self._financing = None
        self._costs_paid = False

    def get_total_value(self) -> int:
        return self._value

    def get_rent(self) -> int:
        return self._rent

    def is_owned(self) -> bool:
        return self._owned

    def buy(self, account: Account):
        if account.get_balance() >= self.get_total_value():
            account.withdraw(self.get_total_value())
        else:
            cash = account.get_balance()
            account.withdraw(cash)
            self._financing = Financing(self.clock, self.get_total_value(), cash)
        self._owned = True

    def pay_costs(self, account: Account) -> int:
        if self.is_owned():
            account.withdraw(
                self.get_total_value() * YEARLY_PROPERTY_MAINTENANCE_COSTS / 12
            )
            if self._financing is not None:
                account.withdraw(self._financing.get_rate())
        else:
            account.withdraw(self.get_rent())
        self._costs_paid = True

    def get_owned_value(self):
        if self.is_owned() and self._financing is None:
            return self.get_total_value()
        elif self.is_owned() and self._financing is not None:
            return (
                self.get_total_value()
                * self._financing.get_total_amortization()
                / self._financing.get_total_amount()
            )
        else:
            return 0

    def onTick(self):
        if not self._costs_paid:
            raise Exception("Costs for property not paid!")
        self._value = self._value * (1 + PROPERTY_VALUE_INCREASE_PER_YEAR) ** (1 / 12)
        self._rent = self._rent * (1 + PROPERTY_VALUE_INCREASE_PER_YEAR) ** (1 / 12)
        self._costs_paid = False
