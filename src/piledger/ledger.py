from piledger.transaction import Transaction

class Ledger:
    """
    Livre de comptes, stocke et gère les transactions.
    """
    def __init__(self) -> None:
        self.transactions: list[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def get_balance(self, compte: str) -> float:
        """
        Calcule le solde d'un compte donné.
        """
        return sum(txn.montant for txn in self.transactions if txn.compte == compte)

    def list_accounts(self) -> set[str]:
        """
        Retourne la liste des comptes existants.
        """
        return {txn.compte for txn in self.transactions}

    def filter_by_account(self, compte: str) -> list[Transaction]:
        """
        Retourne toutes les transactions d'un compte.
        """
        return [txn for txn in self.transactions if txn.compte == compte]
