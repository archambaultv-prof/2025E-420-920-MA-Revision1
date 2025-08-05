# ===== account_manager.py =====
"""
Module pour la gestion des comptes et transactions.
"""

from collections import defaultdict
from typing import List, Dict, Set, Optional
from .models import Transaction, AccountStatistics
from .exceptions import AccountNotFoundError


class AccountManager:
    """
    Gestionnaire principal pour les comptes et transactions.
    """
    
    def __init__(self, transactions: List[Transaction]):
        """
        Initialise le gestionnaire avec une liste de transactions.
        
        Args:
            transactions: Liste des transactions à gérer
        """
        self.transactions = transactions
        self._accounts_cache: Optional[Set[str]] = None
    
    def get_all_accounts(self) -> Set[str]:
        """
        Retourne l'ensemble de tous les comptes uniques.
        
        Returns:
            Set contenant tous les noms de comptes
        """
        if self._accounts_cache is None:
            self._accounts_cache = {t.compte for t in self.transactions}
        return self._accounts_cache
    
    def validate_account_name(self, account_name: str) -> str:
        """
        Valide et retourne le nom de compte correct (insensible à la casse).
        
        Args:
            account_name: Nom du compte à valider
            
        Returns:
            Nom du compte correct
            
        Raises:
            AccountNotFoundError: Si le compte n'existe pas
        """
        accounts = self.get_all_accounts()
        
        for account in accounts:
            if account.lower() == account_name.lower():
                return account
        
        raise AccountNotFoundError(f"Le compte '{account_name}' n'existe pas")
    
    def calculate_balance(self, account_name: str) -> float:
        """
        Calcule le solde d'un compte.
        
        Args:
            account_name: Nom du compte
            
        Returns:
            Solde du compte
        """
        validated_account = self.validate_account_name(account_name)
        return sum(t.montant for t in self.transactions 
                  if t.compte == validated_account)
    
    def get_transactions_by_account(self, account_name: str) -> List[Transaction]:
        """
        Retourne toutes les transactions d'un compte.
        
        Args:
            account_name: Nom du compte
            
        Returns:
            Liste des transactions du compte
        """
        validated_account = self.validate_account_name(account_name)
        return [t for t in self.transactions if t.compte == validated_account]
    
    def get_account_statistics(self, account_name: str) -> AccountStatistics:
        """
        Calcule les statistiques d'un compte.
        
        Args:
            account_name: Nom du compte
            
        Returns:
            Objet AccountStatistics avec les statistiques du compte
        """
        transactions = self.get_transactions_by_account(account_name)
        return AccountStatistics(transactions)
    
    def get_all_balances(self) -> Dict[str, float]:
        """
        Calcule les soldes de tous les comptes.
        
        Returns:
            Dictionnaire {nom_compte: solde}
        """
        balances = defaultdict(float)
        for transaction in self.transactions:
            balances[transaction.compte] += transaction.montant
        return dict(balances)
    
    def search_transactions_by_comment(self, keyword: str) -> List[Transaction]:
        """
        Recherche des transactions par mot-clé dans les commentaires.
        
        Args:
            keyword: Mot-clé à rechercher
            
        Returns:
            Liste des transactions contenant le mot-clé
        """
        keyword_lower = keyword.lower()
        return [t for t in self.transactions 
                if keyword_lower in t.commentaire.lower()]
    
    def get_transactions_by_date_range(self, start_date: str, 
                                     end_date: str) -> List[Transaction]:
        """
        Filtre les transactions par plage de dates.
        
        Args:
            start_date: Date de début (YYYY-MM-DD)
            end_date: Date de fin (YYYY-MM-DD)
            
        Returns:
            Liste des transactions dans la plage de dates
        """
        return [t for t in self.transactions 
                if start_date <= t.date <= end_date]
    
    def get_financial_summary(self) -> Dict[str, float]:
        """
        Calcule un résumé financier global.
        
        Returns:
            Dictionnaire avec les totaux revenus, dépenses, situation nette
        """
        total_income = sum(abs(t.montant) for t in self.transactions if t.is_income())
        total_expenses = sum(t.montant for t in self.transactions if t.is_expense())
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_worth': total_income - total_expenses
        }
    
    def find_largest_expense(self) -> Optional[Transaction]:
        """
        Trouve la plus grande dépense.
        
        Returns:
            Transaction de la plus grande dépense, ou None si aucune
        """
        expenses = [t for t in self.transactions if t.is_expense()]
        return max(expenses, key=lambda x: x.montant) if expenses else None
