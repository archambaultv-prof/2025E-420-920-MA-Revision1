import os

class Transaction:
    """Représente une transaction comptable avec ses propriétés de base."""
    def __init__(self, no_txn, date, compte, montant, commentaire=""):
        self.no_txn = no_txn
        self.date = date
        self.compte = compte
        self.montant = float(montant)
        self.commentaire = commentaire

    def __str__(self):
        return f"{self.date} - {self.compte}: {self.montant:.2f}$"



