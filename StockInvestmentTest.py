import unittest
from StockInvestment import StockInvestment


class StockInvestmentUnitTest(unittest.TestCase):
    def test_total_value(self):
        inv = StockInvestment(0.1, 100000)
        self.assertEqual(round(inv.get_value(), 2), 100000)
        inv.put_deposit(1000)
        inv.step()
        self.assertEqual(round(inv.get_value(), 2), 101797.41)

    # TODO: Add taxes
    def test_pulling_out_money(self):
        inv = StockInvestment(0.1, 1000)
        self.assertEqual(round(inv.get_value(), 2), 1000)
        inv.put_deposit(-1000)
        inv.step()
        self.assertEqual(round(inv.get_value(), 2), 7.97)

    # TODO: Make this also work with negative values. Loan interest rate needed.
