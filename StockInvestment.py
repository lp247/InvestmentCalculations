from typing import Callable
import unittest


class StockInvestment:
    def __init__(self, expected_yield: int, investment: Callable[[int], int]):
        self.expected_yield = expected_yield
        self.investment = investment
        self._total_value_cache = {}

    # TODO: Make this also work with negative values. Loan interest rate needed.
    def get_total_value(self, t: int):
        if t in self._total_value_cache:
            return self._total_value_cache[t]
        if t < 0:
            return 0
        if t == 0:
            return self.investment(0)
        else:
            ret = self.get_total_value(t - 1) * (
                (1 + self.expected_yield) ** (1 / 12)
            ) + self.investment(t)
            self._total_value_cache[t] = ret
            return ret

    # def get_total_value(self, t: int):
    # 1. Get investments until t and save in list
    # 2. Add investment with return to each element at time t (dictionary with start value and value at t)
    # 3. To get total value calculate sum of all the elements' current values
    # 4. Store list of investments in cache at key t
    # 5. If a negative investment comes in
    #    a) Set as much elements, beginning at the front, to 0 until the accumulated value surpasses the negative investment; take taxes when selling into account here
    #    b) Replace the new, previously negative, investment with the remainder of evening out the two values
    # if t < 0:
    # return 0;
    # return


class StockInvestmentUnitTest(unittest.TestCase):
    def test_total_value(self):
        inv = StockInvestment(0.1, lambda t: 100000 if t == 0 else 1000)
        self.assertEqual(inv.get_total_value(0), 100000)
        self.assertEqual(round(inv.get_total_value(1), 2), 101797.41)

    def test_pulling_out_money(self):
        inv = StockInvestment(0.1, lambda t: 1000 if t % 2 == 0 else -1000)
        self.assertEqual(inv.get_total_value(0), 1000)
        self.assertEqual(round(inv.get_total_value(1), 2), 7.97)

    # TODO: Add negative interest
