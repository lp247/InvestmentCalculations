from typing import TypedDict
from .Account import Account
from .Clock import Clock
from .FinancialEntity import FinancialEntity


class FinancingContext(TypedDict):
    interest_rate: float
    initial_amortization_rate: float


class Financing(FinancialEntity):
    def __init__(
        self,
        clock: Clock,
        account: Account,
        total_amount: float,
        context: FinancingContext,
    ):
        super().__init__(clock)
        self.context = context
        self.total_amount = total_amount

        self._rate = 0
        self._interest = 0
        self._amortization = 0
        self._total_interest = 0
        self._total_amortization = 0
        self._remaining_loan = total_amount

        account.deposit(total_amount)

    def get_total_amount(self) -> float:
        return self.total_amount

    def get_rate(self) -> float:
        return self._rate

    def get_interest(self) -> float:
        return self._interest

    def get_amortization(self) -> float:
        return self._amortization

    def get_total_interest(self) -> float:
        return self._total_interest

    def get_total_amortization(self) -> float:
        return self._total_amortization

    def get_remaining_loan(self) -> float:
        return self._remaining_loan

    def get_costs(self) -> float:
        return self.get_rate()

    def get_value(self) -> float:
        return -1 * self.get_remaining_loan()

    def onTick(self) -> None:
        super().onTick()
        interest_rate = self.context["interest_rate"]
        initial_amortization_rate = self.context["initial_amortization_rate"]
        # Is it in reality really only divided by 12?
        annuity = self.total_amount * (interest_rate + initial_amortization_rate) / 12
        remaining_loan = self.get_total_amount() - self.get_total_amortization()
        next_interest = remaining_loan * interest_rate / 12
        next_rate = min(annuity, remaining_loan + next_interest)
        next_amortization = next_rate - next_interest
        next_remaining_loan = remaining_loan - next_amortization
        next_total_interest = self.get_total_interest() + next_interest

        self._rate = next_rate
        self._interest = next_interest
        self._amortization = next_amortization
        self._total_interest = next_total_interest
        self._total_amortization = self.get_total_amount() - next_remaining_loan
        self._remaining_loan = next_remaining_loan
