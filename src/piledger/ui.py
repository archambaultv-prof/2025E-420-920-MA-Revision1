# ===== ui.py =====
"""
Module pour l'interface utilisateur en ligne de commande.
"""

from datetime import datetime
from .account_manager import AccountManager
from .data_manager import CSVDataManager
from .exceptions import AccountNotFoundError, FileError, DataValidationError


class UserInterface:
    """
    Interface utilisateur pour le système de gestion comptable.
    """
    
    def __init__(self, account_manager: AccountManager, data_manager: CSVDataManager):
        """
        Initialise l'interface utilisateur.
        
        Args:
            account_manager: Gestionnaire des comptes
            data_manager: Gestionnaire des données
        """
        self.account_manager = account_manager
        self.data_manager = data_manager
    
    def display_menu(self) -> None:
        """Affiche le menu principal."""
        print("\n" + "="*50)
        print("SYSTÈME DE GESTION COMPTABLE PERSONNEL")
        print("="*50)
        print("1. Afficher le solde d'un compte")
        print("2. Afficher toutes les transactions") 
        print("3. Afficher les transactions d'un compte")
        print("4. Afficher le résumé de tous les comptes")
        print("5. Afficher les statistiques financières")
        print("6. Exporter les écritures d'un compte")
        print("7. Rechercher par période")
        print("8. Rechercher par commentaire")
        print("9. Statistiques détaillées d'un compte")
        print("0. Quitter")
        print("="*50)
    
    def get_user_input(self, prompt: str, required: bool = True) -> str:
        """
        Obtient une entrée utilisateur avec validation.
        
        Args:
            prompt: Message à afficher
            required: Si l'entrée est requise
            
        Returns:
            Entrée utilisateur validée
        """
        while True:
            user_input = input(prompt).strip()
            if not required or user_input:
                return user_input
            print("❌ Cette information est requise!")
    
    def validate_date_format(self, date_string: str) -> bool:
        """
        Valide le format de date YYYY-MM-DD.
        
        Args:
            date_string: Chaîne de date à valider
            
        Returns:
            True si le format est valide
        """
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def display_accounts_list(self) -> None:
        """Affiche la liste des comptes disponibles."""
        accounts = sorted(self.account_manager.get_all_accounts())
        print("\nComptes disponibles:")
        for i, account in enumerate(accounts, 1):
            print(f"  {i}. {account}")
    
    def handle_balance_inquiry(self) -> None:
        """Gère la consultation de solde d'un compte."""
        print("\n--- Consultation de solde ---")
        self.display_accounts_list()
        
        try:
            account_name = self.get_user_input("\nEntrez le nom du compte: ")
            balance = self.account_manager.calculate_balance(account_name)
            validated_account = self.account_manager.validate_account_name(account_name)
            
            print(f"\n Solde du compte '{validated_account}': {balance:.2f}$")
            
            # Statistiques supplémentaires
            stats = self.account_manager.get_account_statistics(validated_account)
            print(f"   Nombre de transactions: {stats.count}")
            print(f"   Montant moyen: {stats.average:.2f}$")
            
        except AccountNotFoundError as e:
            print(f"❌ {e}")
    
    def display_all_transactions(self) -> None:
        """Affiche toutes les transactions."""
        print("\n=== TOUTES LES TRANSACTIONS ===")
        for transaction in self.account_manager.transactions:
            print(transaction)
            if transaction.commentaire:
                print(f"    {transaction.commentaire}")
            print()
    
    def handle_account_transactions(self) -> None:
        """Gère l'affichage des transactions d'un compte."""
        print("\n--- Transactions par compte ---")
        self.display_accounts_list()
        
        try:
            account_name = self.get_user_input("\nEntrez le nom du compte: ")
            transactions = self.account_manager.get_transactions_by_account(account_name)
            validated_account = self.account_manager.validate_account_name(account_name)
            
            if not transactions:
                print(f"❌ Aucune transaction pour le compte '{validated_account}'")
                return
            
            print(f"\n=== TRANSACTIONS POUR '{validated_account}' ===")
            for transaction in transactions:
                print(transaction)
                if transaction.commentaire:
                    print(f"    {transaction.commentaire}")
                print()
            
            balance = self.account_manager.calculate_balance(validated_account)
            print(f" Solde total: {balance:.2f}$")
            
        except AccountNotFoundError as e:
            print(f"❌ {e}")
    
    def display_summary(self) -> None:
        """Affiche le résumé de tous les comptes."""
        print("\n=== RÉSUMÉ DES COMPTES ===")
        balances = self.account_manager.get_all_balances()
        
        for account in sorted(balances.keys()):
            print(f"{account}: {balances[account]:.2f}$")
    
    def handle_statistics(self) -> None:
        """Affiche les statistiques financières globales."""
        print("\n=== STATISTIQUES FINANCIÈRES ===")
        
        summary = self.account_manager.get_financial_summary()
        
        print(f" Revenus totaux: {summary['total_income']:.2f}$")
        print(f" Dépenses totales: {summary['total_expenses']:.2f}$")
        print(f" Situation nette: {summary['net_worth']:.2f}$")
        
        # Indicateur visuel
        net_worth = summary['net_worth']
        if net_worth > 0:
            print(" Situation financière positive")
        elif net_worth < 0:
            print(" Situation financière négative")
        else:
            print("  Situation financière équilibrée")
        
        # Plus grosse dépense
        largest_expense = self.account_manager.find_largest_expense()
        if largest_expense:
            print(f"\n Plus grosse dépense: {largest_expense.montant:.2f}$ ({largest_expense.compte})")
            if largest_expense.commentaire:
                print(f"    {largest_expense.commentaire}")
        
        # Taux d'épargne
        if summary['total_income'] > 0:
            savings_rate = (summary['net_worth'] / summary['total_income']) * 100
            print(f" Taux d'épargne: {savings_rate:.1f}%")
    
    def handle_export(self) -> None:
        """Gère l'exportation des écritures d'un compte."""
        print("\n--- Exportation ---")
        self.display_accounts_list()
        
        try:
            account_name = self.get_user_input("\nEntrez le nom du compte à exporter: ")
            transactions = self.account_manager.get_transactions_by_account(account_name)
            validated_account = self.account_manager.validate_account_name(account_name)
            
            if not transactions:
                print(f"❌ Aucune transaction à exporter pour '{validated_account}'")
                return
            
            # Génère un nom de fichier par défaut
            default_filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
            filename = self.get_user_input(
                f"Nom du fichier (défaut: {default_filename}): ", 
                required=False
            )
            
            if not filename:
                filename = default_filename
            elif not filename.endswith('.csv'):
                filename += '.csv'
            
            self.data_manager.export_transactions(transactions, filename)
            print(f" {len(transactions)} transaction(s) exportée(s) vers {filename}")
            
        except (AccountNotFoundError, FileError) as e:
            print(f"❌ {e}")
    
    def handle_date_search(self) -> None:
        """Gère la recherche par période."""
        print("\n--- Recherche par période ---")
        
        # Validation des dates
        while True:
            start_date = self.get_user_input(" Date de début (YYYY-MM-DD): ")
            if self.validate_date_format(start_date):
                break
            print("❌ Format invalide! Utilisez YYYY-MM-DD")
        
        while True:
            end_date = self.get_user_input(" Date de fin (YYYY-MM-DD): ")
            if self.validate_date_format(end_date):
                break
            print("❌ Format invalide! Utilisez YYYY-MM-DD")
        
        if start_date > end_date:
            print("❌ La date de début doit être antérieure à la date de fin!")
            return
        
        transactions = self.account_manager.get_transactions_by_date_range(start_date, end_date)
        
        if not transactions:
            print(f"❌ Aucune transaction entre {start_date} et {end_date}")
            return
        
        print(f"\n {len(transactions)} transaction(s) trouvée(s):")
        print("-" * 60)
        
        total = 0
        for transaction in transactions:
            print(f" {transaction.date} | {transaction.compte:<20} | {transaction.montant:>8.2f}$")
            if transaction.commentaire:
                print(f"    {transaction.commentaire}")
            total += transaction.montant
        
        print("-" * 60)
        print(f" Total de la période: {total:.2f}$")
    
    def handle_comment_search(self) -> None:
        """Gère la recherche par commentaire."""
        print("\n--- Recherche par commentaire ---")
        
        keyword = self.get_user_input("🔍 Mot-clé à rechercher: ")
        transactions = self.account_manager.search_transactions_by_comment(keyword)
        
        if not transactions:
            print(f"❌ Aucune transaction contenant '{keyword}'")
            return
        
        print(f"\n {len(transactions)} transaction(s) trouvée(s):")
        print("-" * 70)
        
        for transaction in transactions:
            print(f" {transaction.date} | {transaction.compte:<20} | {transaction.montant:>8.2f}$")
            print(f"    {transaction.commentaire}")
            print()
    
    def handle_account_statistics(self) -> None:
        """Affiche les statistiques détaillées d'un compte."""
        print("\n--- Statistiques détaillées ---")
        self.display_accounts_list()
        
        try:
            account_name = self.get_user_input("\nEntrez le nom du compte: ")
            stats = self.account_manager.get_account_statistics(account_name)
            validated_account = self.account_manager.validate_account_name(account_name)
            
            print(f"\n=== STATISTIQUES POUR '{validated_account}' ===")
            print(f" Nombre de transactions: {stats.count}")
            print(f" Montant total: {stats.total:.2f}$")
            print(f" Montant moyen: {stats.average:.2f}$")
            print(f" Montant minimum: {stats.minimum:.2f}$")
            print(f" Montant maximum: {stats.maximum:.2f}$")
            
        except AccountNotFoundError as e:
            print(f"❌ {e}")
    
    def run(self) -> None:
        """Lance l'interface utilisateur principale."""
        print(" Chargement des données...")
        
        try:
            transactions = self.data_manager.load_transactions()
            self.account_manager = AccountManager(transactions)
            print(f" {len(transactions)} transaction(s) chargée(s)")
            
        except (FileError, DataValidationError) as e:
            print(f"❌ Erreur de chargement: {e}")
            return
        
        # Boucle principale
        while True:
            self.display_menu()
            
            try:
                choice = self.get_user_input("\nVotre choix: ")
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir!")
                break
            
            try:
                if choice == "1":
                    self.handle_balance_inquiry()
                elif choice == "2":
                    self.display_all_transactions()
                elif choice == "3":
                    self.handle_account_transactions()
                elif choice == "4":
                    self.display_summary()
                elif choice == "5":
                    self.handle_statistics()
                elif choice == "6":
                    self.handle_export()
                elif choice == "7":
                    self.handle_date_search()
                elif choice == "8":
                    self.handle_comment_search()
                elif choice == "9":
                    self.handle_account_statistics()
                elif choice == "0":
                    print("\n👋 Merci d'avoir utilisé le système!")
                    break
                else:
                    print("❌ Choix invalide!")
                    
            except Exception as e:
                print(f"❌ Erreur inattendue: {e}")
            
            if choice != "0":
                input("\nAppuyez sur Entrée pour continuer...")