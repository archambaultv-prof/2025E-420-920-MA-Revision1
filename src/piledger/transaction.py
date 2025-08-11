from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Transaction:
    """
    Représente une transaction financière.
    """
    date: str
    compte: str
    montant: float
    commentaire: str = ""

    def __str__(self) -> str:
        return f"{self.date} | {self.compte} | {self.montant:.2f} | {self.commentaire}"

    def to_dict(self) -> dict[str, str | float]:
        """
        Convertit l'objet en dictionnaire pour l'export CSV.
        """
        return {
            "Date": self.date,
            "Compte": self.compte,
            "Montant": self.montant,
            "Commentaire": self.commentaire
        }
