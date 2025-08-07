from .file_manager import FileManager
from .transactions_service import TransactionService

class MenuHandler:
    """
    Classe qui gère l'affichage du menu et les interactions utilisateur.
    Elle utilise TransactionService pour exécuter les calculs et FileManager pour l'exportation des données.
    """

    def __init__(self, transaction_service: TransactionService, file_manager: FileManager):
        """
        Initialise la classe avec les services nécessaires.
        :param transaction_service: Service qui manipule les transactions.
        :param file_manager: Service qui gère la lecture et l'écriture des fichiers CSV.
        """
        self.transaction_service = transaction_service
        self.file_manager = file_manager

    def display_menu(self):
        """
        Affiche les différentes options du menu à l'utilisateur.
        """
        print("Menu:")
        print("1. Afficher tous les comptes")
        print("2. Calculer le solde d'un compte")
        print("3. Trouver le revenu total d'un compte")
        print("4. Trouver les dépenses totales d'un compte")
        print("5. Trouver la plus grande dépense d'un compte")
        print("6. Obtenir les transactions par date")
        print("7. Exporter les transactions vers un fichier CSV")
        print("8. Quitter")

    def handle_user_selection(self, selection):
        """
        Exécute l'action correspondant au choix de l'utilisateur.
        :param selection: Numéro du choix effectué par l'utilisateur.
        """
        if selection == 1:
            # Affiche tous les comptes distincts présents dans les transactions
            accounts = self.transaction_service.get_all_accounts()
            print("Comptes:")
            for account in accounts:
                print(f" - {account}")

        elif selection == 2:
            # Calcul du solde d'un compte avec gestion des erreurs (compte inexistant)
            try:
                account_name = input("Entrez le nom du compte: ")
                balance = self.transaction_service.calculate_balance(account_name)
                print(f"Le solde de {account_name} est {balance}.")
            except ValueError as e:
                print(e)

        elif selection == 3:
            # Affiche les revenus totaux pour un compte donné
            try:
                account_name = input("Entrez le nom du compte: ")
                total_income = self.transaction_service.find_total_income(account_name)
                print(f"Le revenu total de {account_name} est {total_income}.")
            except ValueError as e:
                print(e)

        elif selection == 4:
            # Affiche les dépenses totales pour un compte donné
            try:
                account_name = input("Entrez le nom du compte: ")
                total_expenses = self.transaction_service.find_total_expenses(account_name)
                print(f"Les dépenses totales de {account_name} sont {total_expenses}.")
            except ValueError as e:
                print(e)

        elif selection == 5:
            # Affiche la plus grosse dépense d'un compte
            try:
                account_name = input("Entrez le nom du compte: ")
                largest_expense = self.transaction_service.find_largest_expense(account_name)
                if largest_expense:
                    print(f"La plus grande dépense de {account_name} est {largest_expense.montant}.")
                else:
                    print(f"Aucune dépense trouvée pour {account_name}.")
            except ValueError as e:
                print(e)

        elif selection == 6:
            # Liste les transactions pour un compte donné à une date précise
            try:
                account_name = input("Entrez le nom du compte: ")
                date = input("Entrez la date (YYYY-MM-DD): ")
                transactions = self.transaction_service.get_transactions_by_date(account_name, date)
                print(f"Transactions pour {account_name} le {date}:")
                for txn in transactions:
                    print(f" - {txn}")
            except ValueError as e:
                print(e)

        elif selection == 7:
            # Exportation des transactions vers un fichier CSV
            filename = input("Entrez le nom du fichier pour l'exportation: ")
            if not filename.endswith('.csv'):
                filename += '.csv'
            self.file_manager.export_transactions(self.transaction_service.transactions, filename)
            print(f"Transactions exportées vers {filename}.")

        elif selection == 8:
            print("Au revoir!")

        else:
            # Cas d'un choix qui ne correspond à aucune option du menu
            print("Sélection invalide.")
