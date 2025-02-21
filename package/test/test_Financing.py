import unittest
from ..src.Account import Account, AccountContext
from ..src.Clock import Clock
from ..src.Financing import Financing, FinancingContext

test_context: FinancingContext = {
    "interest_rate": 0.036,
    "initial_amortization_rate": 0.02,
}

test_account_context: AccountContext = {
    "initial_cash": 1000000,
    "overdraft_loan_rate": 0.1,
}


class FinancingUnitTest(unittest.TestCase):
    def test_account(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        Financing(clock, account, 250000, test_context)
        self.assertEqual(account.balance, 1250000)

    def test_rate(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_rate(), 0)
        clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 1166.67)
        financing.pay_costs(account)
        account.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 1166.67)
        for _ in range(341):
            financing.pay_costs(account)
            account.pay_costs(account)
            clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 1166.67)
        financing.pay_costs(account)
        account.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 841.55)
        financing.pay_costs(account)
        account.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 0)

    def test_total_amortization(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_total_amortization(), 0)
        clock.tick()
        self.assertEqual(round(financing.get_total_amortization(), 2), 416.67)
        for _ in range(359):
            financing.pay_costs(account)
            account.pay_costs(account)
            clock.tick()
        self.assertEqual(financing.get_total_amortization(), 250000)

    def test_remaining_loan(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_remaining_loan(), 250000)
        clock.tick()
        self.assertEqual(round(financing.get_remaining_loan(), 2), 249583.33)
        for _ in range(120):
            financing.pay_costs(account)
            account.pay_costs(account)
            clock.tick()
        self.assertEqual(round(financing.get_remaining_loan(), 2), 189325.72)

    def test_interest(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_interest(), 0)
        clock.tick()
        self.assertEqual(financing.get_interest(), 750)
        financing.pay_costs(account)
        account.pay_costs(account)
        clock.tick()
        self.assertEqual(financing.get_interest(), 748.75)
        for _ in range(120):
            financing.pay_costs(account)
            account.pay_costs(account)
            clock.tick()
        self.assertEqual(round(financing.get_interest(), 2), 567.98)
        for _ in range(238):
            financing.pay_costs(account)
            account.pay_costs(account)
            clock.tick()
        self.assertEqual(financing.get_interest(), 0)

    def test_total_interest(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_total_interest(), 0)
        clock.tick()
        self.assertEqual(financing.get_total_interest(), 750)
        account.pay_costs(account)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(financing.get_total_interest(), 1498.75)
        for _ in range(358):
            financing.pay_costs(account)
            account.pay_costs(account)
            clock.tick()
        self.assertEqual(round(financing.get_total_interest(), 2), 151008.21)
