class PropertyInvestment:
    def __init__(
        self,
        total_amount: int,
        interest_rate: int,
        initial_amortization_rate: int,
        deductible: int,
    ):
        self._total_amount = total_amount
        self._interest_rate = interest_rate
        # Is it in reality really only divided by 12?
        self._annuity = (
            (total_amount - deductible)
            * (interest_rate + initial_amortization_rate)
            / 12
        )
        self._deductible = deductible

        self._rate = 0
        self._interest = 0
        self._amortization = 0
        self._total_interest = 0
        self._total_amortization = deductible
        self._remaining_loan = total_amount

    def get_total_amount(self):
        return self._total_amount

    def get_rate(self):
        return self._rate

    def get_interest(self):
        return self._interest

    def get_amortization(self):
        return self._amortization

    def get_total_interest(self):
        return self._total_interest

    def get_total_amortization(self):
        return self._total_amortization

    def get_remaining_loan(self):
        return self._remaining_loan

    def step(self):
        remaining_loan = self.get_total_amount() - self.get_total_amortization()
        next_interest = remaining_loan * self._interest_rate / 12
        next_rate = min(self._annuity, remaining_loan + next_interest)
        next_amortization = next_rate - next_interest
        next_remaining_loan = remaining_loan - next_amortization
        next_total_interest = self.get_total_interest() + next_interest

        self._rate = next_rate
        self._interest = next_interest
        self._amortization = next_amortization
        self._total_interest = next_total_interest
        self._total_amortization = self.get_total_amount() - next_remaining_loan
        self._remaining_loan = next_remaining_loan
