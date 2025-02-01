from typing import Callable


class MonthlyBudget:
    def __init__(self):
        self.costs = []

    def get_total_cash(self, t: int):
        return 50000 if t == 0 else 2500

    def add_cost(self, cost: Callable[[int], int]):
        self.costs.append(cost)

    def get_total_costs(self, t: int):
        return sum([cost(t) for cost in self.costs])

    def get_free_cash(self, t: int):
        return self.get_total_cash(t) - self.get_total_costs(t)
