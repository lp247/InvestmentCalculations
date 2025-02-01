import unittest


class PropertyInvestment:
    def __init__(
        self,
        start_at: int,
        total_amount: int,
        interest_rate: int,
        initial_amortization_rate: int,
        deductible: int,
    ):
        self.start_at = start_at
        self.total_amount = total_amount
        self.interest_rate = interest_rate
        self.deductible = deductible
        # Is it in reality really only divided by 12?
        self.annuity = (
            (total_amount - deductible)
            * (interest_rate + initial_amortization_rate)
            / 12
        )
        self._total_amortization_cache = {}
        self._interest_at_cache = {}

    def _get_annuity(self):
        return self.annuity

    def get_rate_at(self, t: int):
        return min(
            self._get_annuity(),
            self.get_remaining_loan(t - 1) * (1 + self.interest_rate / 12),
        )

    def get_total_amortization(self, t: int):
        if t in self._total_amortization_cache:
            return self._total_amortization_cache[t]
        elif t < self.start_at:
            return 0
        else:
            ret = (
                sum(
                    [
                        (self.get_rate_at(i) - self.get_interest_at(i))
                        for i in range(t + 1)
                    ]
                )
                + self.deductible
            )
            self._total_amortization_cache[t] = ret
            return ret

    def get_total_value(self, t: int):
        return self.get_total_amortization(t)

    def get_remaining_loan(self, t: int):
        if t < self.start_at:
            return 0
        else:
            return self.total_amount - self.get_total_amortization(t)

    # Remaining loan (previous month) -> Interest -> Total Amortization -> Remaining loan
    def get_interest_at(self, t: int):
        if t in self._interest_at_cache:
            return self._interest_at_cache[t]
        else:
            # Is it in reality really only divided by 12?
            ret = self.get_remaining_loan(t - 1) * self.interest_rate / 12
            self._interest_at_cache[t] = ret
            return ret

    def get_total_interest(self, t: int):
        return sum([self.get_interest_at(i) for i in range(t + 1)])

    class PropertyInvestmentUnitTest(unittest.TestCase):
        def test_rate(self):
            inv = PropertyInvestment(0, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_rate_at(0), 0)
            self.assertEqual(round(inv.get_rate_at(1), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(2), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(343), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(344), 2), 841.55)
            self.assertEqual(round(inv.get_rate_at(345), 2), 0)

            inv = PropertyInvestment(0, 300000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_rate_at(0), 0)
            self.assertEqual(round(inv.get_rate_at(1), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(2), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(343), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(344), 2), 841.55)
            self.assertEqual(round(inv.get_rate_at(345), 2), 0)

            inv = PropertyInvestment(12, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_rate_at(0), 0)
            self.assertEqual(inv.get_rate_at(12), 0)
            self.assertEqual(round(inv.get_rate_at(13), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(14), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(355), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(356), 2), 841.55)
            self.assertEqual(round(inv.get_rate_at(357), 2), 0)

            inv = PropertyInvestment(12, 300000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_rate_at(0), 0)
            self.assertEqual(inv.get_rate_at(12), 0)
            self.assertEqual(round(inv.get_rate_at(13), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(14), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(355), 2), 1166.67)
            self.assertEqual(round(inv.get_rate_at(356), 2), 841.55)
            self.assertEqual(round(inv.get_rate_at(357), 2), 0)

        def test_total_amortization(self):
            inv = PropertyInvestment(0, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_total_amortization(0), 0)
            self.assertEqual(round(inv.get_total_amortization(1), 2), 416.67)
            self.assertEqual(inv.get_total_amortization(360), 250000)

            inv = PropertyInvestment(0, 250000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_total_amortization(0), 50000)
            self.assertEqual(round(inv.get_total_amortization(1), 2), 50333.33)
            self.assertEqual(inv.get_total_amortization(360), 250000)

            inv = PropertyInvestment(12, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_total_amortization(0), 0)
            self.assertEqual(inv.get_total_amortization(11), 0)
            self.assertEqual(inv.get_total_amortization(12), 0)
            self.assertEqual(round(inv.get_total_amortization(13), 2), 416.67)

            inv = PropertyInvestment(12, 250000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_total_amortization(0), 0)
            self.assertEqual(inv.get_total_amortization(11), 0)
            self.assertEqual(inv.get_total_amortization(12), 50000)
            self.assertEqual(round(inv.get_total_amortization(13), 2), 50333.33)
            self.assertEqual(inv.get_total_amortization(360), 250000)

        def test_remaining_loan(self):
            inv = PropertyInvestment(0, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_remaining_loan(0), 250000)
            self.assertEqual(round(inv.get_remaining_loan(1), 2), 249583.33)
            self.assertEqual(round(inv.get_remaining_loan(121), 2), 189325.72)

            inv = PropertyInvestment(0, 300000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_remaining_loan(0), 250000)
            self.assertEqual(round(inv.get_remaining_loan(1), 2), 249583.33)
            self.assertEqual(round(inv.get_remaining_loan(121), 2), 189325.72)

            inv = PropertyInvestment(12, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_remaining_loan(11), 0)
            self.assertEqual(inv.get_remaining_loan(12), 250000)
            self.assertEqual(round(inv.get_remaining_loan(13), 2), 249583.33)
            self.assertEqual(round(inv.get_remaining_loan(133), 2), 189325.72)

            inv = PropertyInvestment(12, 300000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_remaining_loan(11), 0)
            self.assertEqual(inv.get_remaining_loan(12), 250000)
            self.assertEqual(round(inv.get_remaining_loan(13), 2), 249583.33)
            self.assertEqual(round(inv.get_remaining_loan(133), 2), 189325.72)

        def test_interest(self):
            inv = PropertyInvestment(0, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_interest_at(0), 0)
            self.assertEqual(inv.get_interest_at(1), 750)
            self.assertEqual(inv.get_interest_at(2), 748.75)
            self.assertEqual(round(inv.get_interest_at(122), 2), 567.98)
            self.assertEqual(inv.get_interest_at(360), 0)

            inv = PropertyInvestment(0, 300000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_interest_at(0), 0)
            self.assertEqual(inv.get_interest_at(1), 750)
            self.assertEqual(inv.get_interest_at(2), 748.75)
            self.assertEqual(round(inv.get_interest_at(122), 2), 567.98)
            self.assertEqual(inv.get_interest_at(360), 0)

            inv = PropertyInvestment(12, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_interest_at(12), 0)
            self.assertEqual(inv.get_interest_at(13), 750)
            self.assertEqual(inv.get_interest_at(14), 748.75)
            self.assertEqual(round(inv.get_interest_at(134), 2), 567.98)
            self.assertEqual(inv.get_interest_at(360), 0)

            inv = PropertyInvestment(12, 300000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_interest_at(12), 0)
            self.assertEqual(inv.get_interest_at(13), 750)
            self.assertEqual(inv.get_interest_at(14), 748.75)
            self.assertEqual(round(inv.get_interest_at(134), 2), 567.98)
            self.assertEqual(inv.get_interest_at(360), 0)

        def test_total_interest(self):
            inv = PropertyInvestment(0, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_total_interest(0), 0)
            self.assertEqual(inv.get_total_interest(1), 750)
            self.assertEqual(inv.get_total_interest(2), 1498.75)
            self.assertEqual(round(inv.get_total_interest(360), 2), 151008.21)

            inv = PropertyInvestment(0, 300000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_total_interest(0), 0)
            self.assertEqual(inv.get_total_interest(1), 750)
            self.assertEqual(inv.get_total_interest(2), 1498.75)
            self.assertEqual(round(inv.get_total_interest(360), 2), 151008.21)

            inv = PropertyInvestment(12, 250000, 0.036, 0.02, 0)
            self.assertEqual(inv.get_total_interest(12), 0)
            self.assertEqual(inv.get_total_interest(13), 750)
            self.assertEqual(inv.get_total_interest(14), 1498.75)
            self.assertEqual(round(inv.get_total_interest(360), 2), 151008.21)

            inv = PropertyInvestment(12, 300000, 0.036, 0.02, 50000)
            self.assertEqual(inv.get_total_interest(12), 0)
            self.assertEqual(inv.get_total_interest(13), 750)
            self.assertEqual(inv.get_total_interest(14), 1498.75)
            self.assertEqual(round(inv.get_total_interest(360), 2), 151008.21)
