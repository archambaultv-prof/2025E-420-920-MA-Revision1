# ===== models.py =====
"""
Module contenant les classes de modeles pour le systeme de gestion comptable.
"""
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Transaction:
    """
    Represente une transaction financiere.

    Attributes:
        no_txn: Numero de transaction unique.
        date: Date de la transaction au format YYYY-MM-DD.
        compte: Nom du compte associe
        montant: Montant de la transaction (positif ou negatif).\
        commentaire: Commentaire optionnel pour la transaction.
    """
    no_txn: int
    date: str
    compte: str
    montant: float
    commentaire: str = ""

    def __post_init__(self):
        """ Valide les donnees apres initialisation. """
        if not isinstance(self.no_txn, int) or self.no_txn <= 0:
            raise ValueError("Le numero de transaction doit etre un entier positif.")
        
        if not self.compte.strip():
            raise ValueError("Le nom du compte ne peut pas être vide")
        
        # Validation du format de date
        try:
            datetime.strptime(self.date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("La date doit être au format YYYY-MM-DD")

    def is_income(self) -> bool:
        """Détermine si la transaction est un revenu."""
        return self.compte.lower() == 'revenu'
    
    def is_expense(self) -> bool:
        """Détermine si la transaction est une dépense."""
        return (self.montant > 0 and 
                self.compte.lower() not in ['compte courant', 'revenu'])
    
    def __str__(self) -> str:
        """Représentation string de la transaction."""
        return (f"Transaction {self.no_txn} - {self.date} | "
                f"{self.compte}: {self.montant:.2f}$")


class AccountStatistics:
    """
    Classe pour calculer et stocker les statistiques d'un compte.
    """
    
    def __init__(self, transactions: List[Transaction]):
        """
        Initialise les statistiques basées sur une liste de transactions.
        
        Args:
            transactions: Liste des transactions du compte
        """
        self.transactions = transactions
        self.amounts = [t.montant for t in transactions]
    
    @property
    def count(self) -> int:
        """Nombre de transactions."""
        return len(self.transactions)
    
    @property
    def total(self) -> float:
        """Montant total (somme)."""
        return sum(self.amounts)
    
    @property
    def average(self) -> float:
        """Montant moyen."""
        return self.total / self.count if self.count > 0 else 0.0
    
    @property
    def minimum(self) -> float:
        """Montant minimum."""
        return min(self.amounts) if self.amounts else 0.0
    
    @property
    def maximum(self) -> float:
        """Montant maximum."""
        return max(self.amounts) if self.amounts else 0.0
    
    def __str__(self) -> str:
        """Représentation string des statistiques."""
        return (f"Statistiques: {self.count} transactions, "
                f"Total: {self.total:.2f}$, Moyenne: {self.average:.2f}$")


# ===== exceptions.py =====
"""
Module contenant les exceptions personnalisées pour le système comptable.
"""


class ComptabiliteError(Exception):
    """Exception de base pour le système de comptabilité."""
    pass


class FileError(ComptabiliteError):
    """Exception levée lors d'erreurs de fichier."""
    pass


class DataValidationError(ComptabiliteError):
    """Exception levée lors d'erreurs de validation des données."""
    pass


class AccountNotFoundError(ComptabiliteError):
    """Exception levée quand un compte n'est pas trouvé."""
    pass    