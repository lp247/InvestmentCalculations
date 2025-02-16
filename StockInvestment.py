from Account import Account
from Clock import Clock, TimeVariant
from config import AVERAGE_STOCK_RETURN


class StockInvestment(TimeVariant):
    def __init__(self, clock: Clock, expected_yield=AVERAGE_STOCK_RETURN):
        super().__init__(clock)
        self._investments = []
        self._expected_yield = expected_yield

    def _add_position(self, amount: int):
        self._investments.append({"base": amount, "current": amount})

    def deposit(self, account: Account, amount: int):
        amount = amount if amount >= 0 else account.get_balance()
        self._add_position(amount)
        account.withdraw(amount)

    def attempt_withdrawal(self, account: Account, requested_amount: int) -> int:
        cnt = 0
        while cnt < requested_amount and len(self._investments) > 0:
            next_element = self._investments.pop(0)
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

    def get_value(self) -> int:
        return sum([x["current"] for x in self._investments])

    def onTick(self):
        self._investments = list(
            map(
                lambda x: {
                    "base": x["base"],
                    "current": x["current"] * (1 + self._expected_yield) ** (1 / 12),
                },
                self._investments,
            )
        )
