


class Account:
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"{self.name}: {self.balance:.2f}"
    

