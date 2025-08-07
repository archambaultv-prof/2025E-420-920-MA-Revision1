from .data_manager import DataManager
from .account_manager import AccountManager

def display_menu():
    """Affiche le menu principal."""
    print("\n" + "="*40)
    print("GESTION COMPTABLE SIMPLIFIÉE")
    print("="*40)
    print("1. Voir tous les comptes")
    print("2. Consulter un solde")
    print("3. Voir les transactions d'un compte")
    print("4. Exporter les données")
    print("5. Rechercher par date")
    print("0. Quitter")
    print("="*40)

def main():
    """Point d'entrée principal de l'application."""
    transactions = DataManager.load_transactions()
    
    if not transactions:
        return
    
    account_manager = AccountManager()
    accounts = account_manager.get_accounts(transactions)
    
    while True:
        display_menu()
        choice = input("Votre choix : ")
        
        if choice == "1":
            print("\nListe des comptes :")
            for account in accounts:
                print(f"- {account}")
                
        elif choice == "2":
            account = input("Nom du compte : ")
            valid_account = account_manager.validate_account(accounts, account)
            if valid_account:
                balance = account_manager.get_balance(transactions, valid_account)
                print(f"\nSolde du compte {valid_account} : {balance:.2f}€")
            else:
                print("Compte introuvable")
                
        elif choice == "3":
            account = input("Nom du compte : ")
            valid_account = account_manager.validate_account(accounts, account)
            if valid_account:
                print(f"\nTransactions du compte {valid_account} :")
                for t in account_manager.get_transactions_by_account(transactions, valid_account):
                    print(t)
            else:
                print("Compte introuvable")
                
        elif choice == "4":
            account = input("Nom du compte à exporter : ")
            valid_account = account_manager.validate_account(accounts, account)
            if valid_account:
                filename = input("Nom du fichier (ex: export.csv) : ") or f"export_{valid_account}.csv"
                DataManager.export_transactions(transactions, valid_account, filename)
            else:
                print("Compte introuvable")
                
        elif choice == "5":
            start = input("Date de début (AAAA-MM-JJ) : ")
            end = input("Date de fin (AAAA-MM-JJ) : ")
            print("\nRésultats :")
            for t in account_manager.get_transactions_by_date(transactions, start, end):
                print(t)
                
        elif choice == "0":
            print("Au revoir !")
            break
            
        else:
            print("Choix invalide")

if __name__ == "__main__":
    main()