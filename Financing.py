from Clock import Clock, TimeVariant
from config import LOAN_INTEREST_RATE, INITIAL_LOAN_AMORTIZATION_RATE


class Financing(TimeVariant):
    def __init__(
        self,
        clock: Clock,
        total_amount: int,
        deductible: int,
        interest_rate=LOAN_INTEREST_RATE,
        initial_amortization_rate=INITIAL_LOAN_AMORTIZATION_RATE,
    ):
        super().__init__(clock)
        self._total_amount = total_amount
        self._interest_rate = interest_rate
        self._initial_amortization_rate = initial_amortization_rate
        # Is it in reality really only divided by 12?
        self._annuity = (
            (total_amount - deductible)
            * (self._interest_rate + self._initial_amortization_rate)
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

    def onTick(self):
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
