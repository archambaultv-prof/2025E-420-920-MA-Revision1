
from .file_manager import FileManager

class TransactionService:
    """
    Classe responsable des opérations liées aux transactions.
    Elle utilise le FileManager pour lire les données du fichier CSV
    et offre des méthodes pour interroger et manipuler ces transactions.
    """
    
    def __init__(self, file_manager: FileManager):
        # On charge toutes les transactions dès l'initialisation à partir du fichier CSV.
        self.transactions = file_manager.read_transactions()

    def account_exists(self, account_name):
        """
        Vérifie si un compte existe parmi les transactions.
        La comparaison est insensible à la casse et aux espaces.
        """
        return any(
            t.compte.strip().lower() == account_name.strip().lower()
            for t in self.transactions
        )

    def get_all_accounts(self):
        """
        Retourne un ensemble unique de tous les noms de comptes trouvés dans les transactions.
        """
        return {txn.compte for txn in self.transactions}

    def calculate_balance(self, account_name):
        """
        Calcule le solde total d'un compte (revenus - dépenses).
        Lève une exception si le compte n'existe pas.
        """
        if not self.account_exists(account_name):
            raise ValueError(f"Le compte '{account_name}' n'existe pas.")
        return sum(
            t.montant for t in self.transactions
            if t.compte.strip().lower() == account_name.strip().lower()
        )

    def find_total_income(self, account_name):
        """
        Calcule la somme totale des revenus (transactions positives) pour un compte donné.
        """
        if not self.account_exists(account_name):
            raise ValueError(f"Le compte '{account_name}' n'existe pas.")
        return sum(
            t.montant for t in self.transactions
            if t.montant > 0 and t.compte.strip().lower() == account_name.strip().lower()
        )

    def find_total_expenses(self, account_name):
        """
        Calcule le total des dépenses (montants négatifs).
        Les montants sont convertis en valeurs absolues.
        """
        if not self.account_exists(account_name):
            raise ValueError(f"Le compte '{account_name}' n'existe pas.")
        return sum(
            abs(t.montant) for t in self.transactions
            if t.montant < 0 and t.compte.strip().lower() == account_name.strip().lower()
        )

    def find_largest_expense(self, account_name):
        """
        Trouve la plus grosse dépense (valeur la plus négative) pour un compte donné.
        Retourne None s’il n’y a aucune dépense.
        """
        if not self.account_exists(account_name):
            raise ValueError(f"Le compte '{account_name}' n'existe pas.")
        expenses = [
            t for t in self.transactions
            if t.montant < 0 and t.compte.strip().lower() == account_name.strip().lower()
        ]
        return min(expenses, key=lambda t: t.montant) if expenses else None

    def get_transactions_by_date(self, account_name, date):
        """
        Retourne toutes les transactions d’un compte spécifique effectuées à une date donnée.
        """
        if not self.account_exists(account_name):
            raise ValueError(f"Le compte '{account_name}' n'existe pas.")
        return [
            t for t in self.transactions
            if t.date == date and t.compte.strip().lower() == account_name.strip().lower()
        ]
