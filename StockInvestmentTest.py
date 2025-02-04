import unittest
from StockInvestment import StockInvestment


class StockInvestmentUnitTest(unittest.TestCase):
    def test_total_value(self):
        inv = StockInvestment(0.1, 100000)
        self.assertEqual(round(inv.get_value(), 2), 100000)
        inv.step()
        inv.deposit(1000)
        self.assertEqual(round(inv.get_value(), 2), 101797.41)

    def test_withdraw(self):
        inv = StockInvestment(0.1, 700)
        inv.deposit(300)
        inv.step()
        self.assertEqual(round(inv.get_value(), 2), 1007.97)
        withdrawal = inv.attempt_withdrawal(500)
        self.assertEqual(round(withdrawal, 2), 500)
        self.assertEqual(round(inv.get_value(), 2), 506.58)

    def test_withdraw_too_much(self):
        inv = StockInvestment(0.1, 1000)
        withdrawal = inv.attempt_withdrawal(5000)
        self.assertEqual(round(withdrawal, 2), 1000)
        self.assertEqual(round(inv.get_value(), 2), 0)

    def test_withdraw_over_multiple_positions(self):
        inv = StockInvestment(0.1, 1000)
        inv.deposit(1000)
        inv.deposit(1000)
        self.assertEqual(round(inv.get_value(), 2), 3000)
        inv.step()
        self.assertEqual(round(inv.get_value(), 2), 3023.92)
        withdrawal = inv.attempt_withdrawal(1200)
        self.assertEqual(round(withdrawal, 2), 1200)
        self.assertEqual(round(inv.get_value(), 2), 1819.94)

    # TODO: Make this also work with negative values. Loan interest rate needed.
