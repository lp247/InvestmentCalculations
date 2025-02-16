import unittest
from Clock import Clock
from Financing import Financing


class FinancingUnitTest(unittest.TestCase):
    def test_rate(self):
        clock = Clock()
        inv = Financing(clock, 250000, 0, 0.036, 0.02)
        self.assertEqual(inv.get_rate(), 0)
        clock.tick()
        self.assertEqual(round(inv.get_rate(), 2), 1166.67)
        clock.tick()
        self.assertEqual(round(inv.get_rate(), 2), 1166.67)
        for _ in range(341):
            clock.tick()
        self.assertEqual(round(inv.get_rate(), 2), 1166.67)
        clock.tick()
        self.assertEqual(round(inv.get_rate(), 2), 841.55)
        clock.tick()
        self.assertEqual(round(inv.get_rate(), 2), 0)

    def test_total_amortization(self):
        clock = Clock()
        inv = Financing(clock, 250000, 0, 0.036, 0.02)
        self.assertEqual(inv.get_total_amortization(), 0)
        clock.tick()
        self.assertEqual(round(inv.get_total_amortization(), 2), 416.67)
        for _ in range(359):
            clock.tick()
        self.assertEqual(inv.get_total_amortization(), 250000)

    def test_remaining_loan(self):
        clock = Clock()
        inv = Financing(clock, 250000, 0, 0.036, 0.02)
        self.assertEqual(inv.get_remaining_loan(), 250000)
        clock.tick()
        self.assertEqual(round(inv.get_remaining_loan(), 2), 249583.33)
        for _ in range(120):
            clock.tick()
        self.assertEqual(round(inv.get_remaining_loan(), 2), 189325.72)

    def test_interest(self):
        clock = Clock()
        inv = Financing(clock, 250000, 0, 0.036, 0.02)
        self.assertEqual(inv.get_interest(), 0)
        clock.tick()
        self.assertEqual(inv.get_interest(), 750)
        clock.tick()
        self.assertEqual(inv.get_interest(), 748.75)
        for _ in range(120):
            clock.tick()
        self.assertEqual(round(inv.get_interest(), 2), 567.98)
        for _ in range(238):
            clock.tick()
        self.assertEqual(inv.get_interest(), 0)

    def test_total_interest(self):
        clock = Clock()
        inv = Financing(clock, 250000, 0, 0.036, 0.02)
        self.assertEqual(inv.get_total_interest(), 0)
        clock.tick()
        self.assertEqual(inv.get_total_interest(), 750)
        clock.tick()
        self.assertEqual(inv.get_total_interest(), 1498.75)
        for _ in range(358):
            clock.tick()
        self.assertEqual(round(inv.get_total_interest(), 2), 151008.21)

    def test_deductible(self):
        clock = Clock()
        inv = Financing(clock, 300000, 50000, 0.036, 0.02)
        self.assertEqual(inv.get_total_amortization(), 50000)
        clock.tick()
        self.assertEqual(round(inv.get_total_amortization(), 2), 50416.67)
        for _ in range(359):
            clock.tick()
        self.assertEqual(inv.get_total_amortization(), 300000)
