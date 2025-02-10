from Account import Account
from Financing import Financing
from config import (
    PROPERTY_VALUE_INCREASE_PER_YEAR,
    RENT_PER_SQUARE_METER,
    PRICE_PER_SQUARE_METER,
)


class Property:
    def __init__(self, area: int):
        self._price = area * PRICE_PER_SQUARE_METER
        self._rent = area * RENT_PER_SQUARE_METER
        self._owned = False
        self._financing = None

    def get_price(self) -> int:
        return self._price

    def get_rent(self) -> int:
        return self._rent

    def is_owned(self) -> bool:
        return self._owned

    def buy(self, account: Account):
        if account.get_balance() >= self.get_price():
            account.withdraw(self.get_price())
        else:
            cash = account.get_balance()
            account.withdraw(cash)
            self._financing = Financing(self.get_price(), cash)
        self._owned = True

    def pay_costs(self, account: Account) -> int:
        if self.is_owned() and self._financing is not None:
            account.withdraw(self._financing.get_rate())
        elif not self.is_owned():
            account.withdraw(self.get_rent())

    def get_value(self):
        if self.is_owned() and self._financing is None:
            return self.get_price()
        elif self.is_owned() and self._financing is not None:
            return (
                self.get_price()
                * self._financing.get_total_amortization()
                / self._financing.get_total_amount()
            )
        else:
            return 0

    def step(self):
        if self._financing is not None:
            self._financing.step()
        self._price = self._price * (1 + PROPERTY_VALUE_INCREASE_PER_YEAR) ** (1 / 12)
        self._rent = self._rent * (1 + PROPERTY_VALUE_INCREASE_PER_YEAR) ** (1 / 12)
        pass
