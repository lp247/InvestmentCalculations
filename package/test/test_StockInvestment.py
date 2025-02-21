import unittest
from ..src.Account import Account, AccountContext
from ..src.Clock import Clock
from ..src.StockInvestment import StockInvestment, StockInvestmentContext

test_context: StockInvestmentContext = {
    "expected_yield": 0.1,
    "reinvest_interval": 1000000,
}

test_account_context: AccountContext = {
    "initial_cash": 101000,
    "overdraft_loan_rate": 0.1,
}


class StockInvestmentUnitTest(unittest.TestCase):
    def test_total_value(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 100000)
        self.assertEqual(round(inv.get_value(), 2), 100000)
        clock.tick()
        inv.deposit(account, 1000)
        self.assertEqual(round(inv.get_value(), 2), 101797.41)

    def test_withdraw(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 700)
        inv.deposit(account, 300)
        clock.tick()
        self.assertEqual(round(inv.get_value(), 2), 1007.97)
        withdrawal = inv.attempt_withdrawal(account, 500)
        self.assertEqual(round(withdrawal, 2), 500)
        self.assertEqual(round(inv.get_value(), 2), 506.58)

    def test_withdraw_too_much(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 1000)
        withdrawal = inv.attempt_withdrawal(account, 5000)
        self.assertEqual(round(withdrawal, 2), 1000)
        self.assertEqual(round(inv.get_value(), 2), 0)

    def test_withdraw_over_multiple_positions(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 1000)
        inv.deposit(account, 1000)
        inv.deposit(account, 1000)
        self.assertEqual(round(inv.get_value(), 2), 3000)
        clock.tick()
        self.assertEqual(round(inv.get_value(), 2), 3023.92)
        withdrawal = inv.attempt_withdrawal(account, 1200)
        self.assertEqual(round(withdrawal, 2), 1200)
        self.assertEqual(round(inv.get_value(), 2), 1819.94)

    def test_reinvesting(self):
        test_context: StockInvestmentContext = {
            "expected_yield": 0.1,
            "reinvest_interval": 1,
        }
        clock = Clock()
        account = Account(clock, test_account_context)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 100000)
        self.assertAlmostEqual(inv.get_value(), 100000, 2)
        clock.tick()
        self.assertAlmostEqual(inv.get_value(), 100598.06, 2)
