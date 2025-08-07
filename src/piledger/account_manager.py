from .models import Transaction

class AccountManager:
    """Gère les opérations liées aux comptes et transactions."""
    
    @staticmethod
    def get_accounts(transactions):
        """Retourne la liste des comptes uniques."""
        return sorted({t.compte for t in transactions})
    
    @staticmethod
    def get_balance(transactions, account_name):
        """Calcule le solde d'un compte."""
        return sum(t.montant for t in transactions if t.compte == account_name)
    
    @staticmethod
    def get_transactions_by_account(transactions, account_name):
        """Filtre les transactions par compte."""
        return [t for t in transactions if t.compte == account_name]
    
    @staticmethod
    def get_transactions_by_date(transactions, start_date, end_date):
        """Filtre les transactions par période."""
        return [t for t in transactions if start_date <= t.date <= end_date]
    
    @staticmethod
    def validate_account(accounts, input_name):
        """Valide qu'un compte existe (insensible à la casse)."""
        for account in accounts:
            if account.lower() == input_name.lower():
                return account
        return None