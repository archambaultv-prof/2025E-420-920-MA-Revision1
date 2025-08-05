from datetime import datetime

"""
Représente une transaction financière avec validation du montant et parsing de la date.
"""

class Transaction:
    def __init__(self, no_txn, date, compte, montant, commentaire):
        if not isinstance(montant, (int, float)):
            raise ValueError("Le montant doit être un nombre.")
        
        self.no_txn = no_txn
        self.date = self._parse_date(date)
        self.compte = compte
        self.montant = float(montant)
        self.commentaire = commentaire
        

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date invalide. Format attendu : YYYY-MM-DD")
    
    def to_dict(self) -> dict:
        """
        Convertit l'objet en dictionnaire (utile pour export CSV).
        """
        return {
            'no_txn': self.no_txn,
            'date': self.date.strftime("%Y-%m-%d"),
            'compte': self.compte,
            'montant': self.montant,
            'commentaire': self.commentaire,
        }

    def __str__(self) -> str:
        """
        Retourne une représentation lisible de la transaction.
        """
        base = f"Transaction {self.no_txn} - {self.date.date()}\n  Compte: {self.compte}\n  Montant: {self.montant:.2f}$"
        if self.commentaire:
            base += f"\n  Commentaire: {self.commentaire}"
        return base