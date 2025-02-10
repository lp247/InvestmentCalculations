class Account:
    def __init__(self, initial: int):
        self._balance = initial

    def get_balance(self) -> int:
        return self._balance

    def deposit(self, amount: int):
        self._balance += amount

    def withdraw(self, amount: int):
        if amount > self._balance:
            raise Exception(
                "Cannot withdraw more than is available: Available "
                + str(self._balance)
                + ", Requested: "
                + str(amount)
            )
        self._balance -= amount
