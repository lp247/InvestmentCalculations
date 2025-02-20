import unittest
from .Account import Account
from .Clock import Clock
from .Financing import Financing, FinancingContext

test_context: FinancingContext = {
    "interest_rate": 0.036,
    "initial_amortization_rate": 0.02,
}


class FinancingUnitTest(unittest.TestCase):
    def test_account(self):
        clock = Clock()
        account = Account(clock, 3000)
        Financing(clock, account, 250000, test_context)
        self.assertEqual(account.balance, 253000)

    def test_rate(self):
        clock = Clock()
        account = Account(clock, 3000000)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_rate(), 0)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 1166.67)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 1166.67)
        for _ in range(341):
            financing.pay_costs(account)
            clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 1166.67)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 841.55)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_rate(), 2), 0)

    def test_total_amortization(self):
        clock = Clock()
        account = Account(clock, 3000000)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_total_amortization(), 0)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_total_amortization(), 2), 416.67)
        for _ in range(359):
            financing.pay_costs(account)
            clock.tick()
        self.assertEqual(financing.get_total_amortization(), 250000)

    def test_remaining_loan(self):
        clock = Clock()
        account = Account(clock, 3000000)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_remaining_loan(), 250000)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(round(financing.get_remaining_loan(), 2), 249583.33)
        for _ in range(120):
            financing.pay_costs(account)
            clock.tick()
        self.assertEqual(round(financing.get_remaining_loan(), 2), 189325.72)

    def test_interest(self):
        clock = Clock()
        account = Account(clock, 3000000)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_interest(), 0)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(financing.get_interest(), 750)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(financing.get_interest(), 748.75)
        for _ in range(120):
            financing.pay_costs(account)
            clock.tick()
        self.assertEqual(round(financing.get_interest(), 2), 567.98)
        for _ in range(238):
            financing.pay_costs(account)
            clock.tick()
        self.assertEqual(financing.get_interest(), 0)

    def test_total_interest(self):
        clock = Clock()
        account = Account(clock, 3000000)
        financing = Financing(clock, account, 250000, test_context)
        self.assertEqual(financing.get_total_interest(), 0)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(financing.get_total_interest(), 750)
        financing.pay_costs(account)
        clock.tick()
        self.assertEqual(financing.get_total_interest(), 1498.75)
        for _ in range(358):
            financing.pay_costs(account)
            clock.tick()
        self.assertEqual(round(financing.get_total_interest(), 2), 151008.21)
