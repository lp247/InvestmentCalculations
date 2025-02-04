class StockInvestment:
    def __init__(self, expected_yield: int, initial: int):
        self._value = initial
        self._expected_yield = expected_yield
        self._next_deposit = 0

    def put_deposit(self, amount: int):
        self._next_deposit = amount

    def get_value(self):
        return self._value

    def step(self):
        self._value = (
            self._value * (1 + self._expected_yield) ** (1 / 12) + self._next_deposit
        )
        self._next_deposit = 0
