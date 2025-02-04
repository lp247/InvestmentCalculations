class StockInvestment:
    def __init__(self, expected_yield: int, initial: int):
        self._investments = []
        self.deposit(initial)
        self._expected_yield = expected_yield

    def deposit(self, amount: int):
        self._investments.append({"base": amount, "current": amount})

    def attempt_withdrawal(self, requested_amount: int) -> int:
        cnt = 0
        tax = 0
        while cnt < requested_amount and len(self._investments) > 0:
            next_element = self._investments.pop(0)
            next_current = next_element["current"]
            next_base = next_element["base"]
            revenue = next_current - next_base
            amount_after_tax = 0.75 * revenue + next_base
            cnt += amount_after_tax
            tax += next_current - amount_after_tax
        if cnt > requested_amount:
            self.deposit(cnt - requested_amount)
            cnt = requested_amount
        print("Total Tax Paid: ", str(tax))
        return cnt

    def get_value(self) -> int:
        return sum([x["current"] for x in self._investments])

    def step(self):
        self._investments = list(
            map(
                lambda x: {
                    "base": x["base"],
                    "current": x["current"] * (1 + self._expected_yield) ** (1 / 12),
                },
                self._investments,
            )
        )
