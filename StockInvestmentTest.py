import unittest
from Account import Account
from StockInvestment import StockInvestment


class StockInvestmentUnitTest(unittest.TestCase):
    def test_total_value(self):
        account = Account(101000)
        inv = StockInvestment(0.1)
        inv.deposit(account, 100000)
        self.assertEqual(round(inv.get_value(), 2), 100000)
        inv.step()
        inv.deposit(account, 1000)
        self.assertEqual(round(inv.get_value(), 2), 101797.41)

    def test_withdraw(self):
        account = Account(1000)
        inv = StockInvestment(0.1)
        inv.deposit(account, 700)
        inv.deposit(account, 300)
        inv.step()
        self.assertEqual(round(inv.get_value(), 2), 1007.97)
        withdrawal = inv.attempt_withdrawal(account, 500)
        self.assertEqual(round(withdrawal, 2), 500)
        self.assertEqual(round(inv.get_value(), 2), 506.58)

    def test_withdraw_too_much(self):
        account = Account(1000)
        inv = StockInvestment(0.1)
        inv.deposit(account, 1000)
        withdrawal = inv.attempt_withdrawal(account, 5000)
        self.assertEqual(round(withdrawal, 2), 1000)
        self.assertEqual(round(inv.get_value(), 2), 0)

    def test_withdraw_over_multiple_positions(self):
        account = Account(3000)
        inv = StockInvestment(0.1)
        inv.deposit(account, 1000)
        inv.deposit(account, 1000)
        inv.deposit(account, 1000)
        self.assertEqual(round(inv.get_value(), 2), 3000)
        inv.step()
        self.assertEqual(round(inv.get_value(), 2), 3023.92)
        withdrawal = inv.attempt_withdrawal(account, 1200)
        self.assertEqual(round(withdrawal, 2), 1200)
        self.assertEqual(round(inv.get_value(), 2), 1819.94)

    # TODO: Make this also work with negative values. Loan interest rate needed.
