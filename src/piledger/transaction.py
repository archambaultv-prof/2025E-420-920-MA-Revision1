


class Transaction:
    def __init__(self, no_txn, date, account, amount, comment=None):
        self.no_txn = no_txn
        self.date = date
        self.account = account  # Objet Account
        self.amount = amount
        self.comment = comment

    def __repr__(self):
        return f"Transaction(no_txn={self.no_txn}, date={self.date}, account={self.account.name}, amount={self.amount}, comment={self.comment})"