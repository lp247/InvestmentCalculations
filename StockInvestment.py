from typing import List, TypedDict
from Account import Account
from Clock import Clock
from ValuedEntity import ValuedEntity


class StockInvestmentContext(TypedDict):
    expected_yield: float


class SingleInvestment(TypedDict):
    base: float
    current: float


class StockInvestment(ValuedEntity):
    def __init__(self, clock: Clock, context: StockInvestmentContext):
        super().__init__(clock)
        self.investments: List[SingleInvestment] = []
        self.context = context

    def _add_position(self, amount: float) -> None:
        self.investments.append({"base": amount, "current": amount})

    def deposit(self, account: Account, amount: float) -> None:
        amount = amount if amount >= 0 else account.balance
        self._add_position(amount)
        account.withdraw(amount)

    def attempt_withdrawal(self, account: Account, requested_amount: float) -> float:
        cnt = 0
        while cnt < requested_amount and len(self.investments) > 0:
            next_element = self.investments.pop(0)
            next_current = next_element["current"]
            next_base = next_element["base"]
            revenue = next_current - next_base
            amount_after_tax = 0.75 * revenue + next_base
            cnt += amount_after_tax
        if cnt > requested_amount:
            self._add_position(cnt - requested_amount)
            cnt = requested_amount
        account.deposit(cnt)
        return cnt

    def get_costs(self) -> float:
        return 0

    def get_value(self) -> float:
        return sum([x["current"] for x in self.investments])

    def onTick(self) -> None:
        super().onTick()
        self.investments = list(
            map(
                lambda x: {
                    "base": x["base"],
                    "current": x["current"]
                    * (1 + self.context["expected_yield"]) ** (1 / 12),
                },
                self.investments,
            )
        )
