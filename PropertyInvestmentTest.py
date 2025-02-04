import unittest
from PropertyInvestment import PropertyInvestment


class PropertyInvestmentUnitTest(unittest.TestCase):
    def test_rate(self):
        inv = PropertyInvestment(250000, 0.036, 0.02, 0)
        self.assertEqual(inv.get_rate(), 0)
        inv.step()
        self.assertEqual(round(inv.get_rate(), 2), 1166.67)
        inv.step()
        self.assertEqual(round(inv.get_rate(), 2), 1166.67)
        for _ in range(341):
            inv.step()
        self.assertEqual(round(inv.get_rate(), 2), 1166.67)
        inv.step()
        self.assertEqual(round(inv.get_rate(), 2), 841.55)
        inv.step()
        self.assertEqual(round(inv.get_rate(), 2), 0)

    def test_total_amortization(self):
        inv = PropertyInvestment(250000, 0.036, 0.02, 0)
        self.assertEqual(inv.get_total_amortization(), 0)
        inv.step()
        self.assertEqual(round(inv.get_total_amortization(), 2), 416.67)
        for _ in range(359):
            inv.step()
        self.assertEqual(inv.get_total_amortization(), 250000)

    def test_remaining_loan(self):
        inv = PropertyInvestment(250000, 0.036, 0.02, 0)
        self.assertEqual(inv.get_remaining_loan(), 250000)
        inv.step()
        self.assertEqual(round(inv.get_remaining_loan(), 2), 249583.33)
        for _ in range(120):
            inv.step()
        self.assertEqual(round(inv.get_remaining_loan(), 2), 189325.72)

    def test_interest(self):
        inv = PropertyInvestment(250000, 0.036, 0.02, 0)
        self.assertEqual(inv.get_interest(), 0)
        inv.step()
        self.assertEqual(inv.get_interest(), 750)
        inv.step()
        self.assertEqual(inv.get_interest(), 748.75)
        for _ in range(120):
            inv.step()
        self.assertEqual(round(inv.get_interest(), 2), 567.98)
        for _ in range(238):
            inv.step()
        self.assertEqual(inv.get_interest(), 0)

    def test_total_interest(self):
        inv = PropertyInvestment(250000, 0.036, 0.02, 0)
        self.assertEqual(inv.get_total_interest(), 0)
        inv.step()
        self.assertEqual(inv.get_total_interest(), 750)
        inv.step()
        self.assertEqual(inv.get_total_interest(), 1498.75)
        for _ in range(358):
            inv.step()
        self.assertEqual(round(inv.get_total_interest(), 2), 151008.21)

    def test_deductible(self):
        inv = PropertyInvestment(300000, 0.036, 0.02, 50000)
        self.assertEqual(inv.get_total_amortization(), 50000)
        inv.step()
        self.assertEqual(round(inv.get_total_amortization(), 2), 50416.67)
        for _ in range(359):
            inv.step()
        self.assertEqual(inv.get_total_amortization(), 300000)
