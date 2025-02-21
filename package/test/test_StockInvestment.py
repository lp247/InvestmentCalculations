import unittest
from ..src.Account import Account
from ..src.Clock import Clock
from ..src.StockInvestment import StockInvestment, StockInvestmentContext

test_context: StockInvestmentContext = {
    "expected_yield": 0.1,
}


class StockInvestmentUnitTest(unittest.TestCase):
    def test_total_value(self):
        clock = Clock()
        account = Account(clock, 101000)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 100000)
        self.assertEqual(round(inv.get_value(), 2), 100000)
        inv.pay_costs(account)
        clock.tick()
        inv.deposit(account, 1000)
        self.assertEqual(round(inv.get_value(), 2), 101797.41)

    def test_withdraw(self):
        clock = Clock()
        account = Account(clock, 1000)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 700)
        inv.deposit(account, 300)
        inv.pay_costs(account)
        clock.tick()
        self.assertEqual(round(inv.get_value(), 2), 1007.97)
        withdrawal = inv.attempt_withdrawal(account, 500)
        self.assertEqual(round(withdrawal, 2), 500)
        self.assertEqual(round(inv.get_value(), 2), 506.58)

    def test_withdraw_too_much(self):
        clock = Clock()
        account = Account(clock, 1000)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 1000)
        withdrawal = inv.attempt_withdrawal(account, 5000)
        self.assertEqual(round(withdrawal, 2), 1000)
        self.assertEqual(round(inv.get_value(), 2), 0)

    def test_withdraw_over_multiple_positions(self):
        clock = Clock()
        account = Account(clock, 3000)
        inv = StockInvestment(clock, test_context)
        inv.deposit(account, 1000)
        inv.deposit(account, 1000)
        inv.deposit(account, 1000)
        self.assertEqual(round(inv.get_value(), 2), 3000)
        inv.pay_costs(account)
        clock.tick()
        self.assertEqual(round(inv.get_value(), 2), 3023.92)
        withdrawal = inv.attempt_withdrawal(account, 1200)
        self.assertEqual(round(withdrawal, 2), 1200)
        self.assertEqual(round(inv.get_value(), 2), 1819.94)

    # TODO: Make this also work with negative values. Loan interest rate needed.
