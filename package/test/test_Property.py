import unittest
from ..src.Account import Account, AccountContext
from ..src.Clock import Clock
from ..src.Property import Property, PropertyContext

test_context: PropertyContext = {
    "area": 100,
    "price_per_square_meter": 4000,
    "monthly_rent_per_square_meter": 4000 / 25 / 12,
    "yearly_value_increase_percentage": 0.05,
    "yearly_maintenance_costs_percentage": 0.01,
    "property_purchase_tax_rate": 0.05,
    "property_purchase_notary_cost_rate": 0.02,
    "property_purchase_brokerage": 0.04,
}

test_account_context: AccountContext = {
    "initial_cash": 1000000,
    "overdraft_loan_rate": 0.1,
}


class PropertyUnitTest(unittest.TestCase):
    def test_inherent_value_and_rent(self):
        clock = Clock()
        prop = Property(clock, test_context)
        self.assertEqual(prop.value, 400000)
        self.assertAlmostEqual(prop.monthly_rent, 1333.33, 2)
        clock.tick()
        self.assertAlmostEqual(prop.value, 401629.65, 2)
        self.assertAlmostEqual(prop.monthly_rent, 1338.77, 2)

    def test_purchase(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        prop = Property(clock, test_context)
        self.assertEqual(prop.get_value(), 0)
        self.assertFalse(prop.owned)
        prop.buy(account)
        self.assertEqual(prop.get_value(), 400000)
        self.assertEqual(account.balance, 556000)
        self.assertTrue(prop.owned)

    def test_get_costs(self):
        clock = Clock()
        account = Account(clock, test_account_context)
        prop = Property(clock, test_context)
        self.assertAlmostEqual(prop.get_costs(), 1333.33, 2)
        prop.buy(account)
        self.assertAlmostEqual(prop.get_costs(), 333.33, 2)
