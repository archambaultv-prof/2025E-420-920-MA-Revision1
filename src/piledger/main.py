import os
from piledger.data_handler import read_data_file, handle_export
from piledger.transactions import Transaction
from piledger.accounts import Account
from piledger.ui import display_summary, display_menu
from piledger.statistics import handle_balance_inquiry, handle_statistics, handle_date_search



def main():
    print("Chargement des données...")
    
    if not os.path.exists('data.csv'):
        print("ERREUR: Le fichier data.csv est introuvable!")
        print("Assurez-vous que le fichier se trouve à la racine du répertoire.")
        return
    
    data = read_data_file()
    
    if len(data) == 0:
        print("ERREUR: Aucune donnée n'a pu être chargée!")
        return
    
    print(f"✅ {len(data)} transactions chargées avec succès!")
    
    t = Transaction(data)
    ac = Account(data)
    accounts = ac.get_all_accounts()
    
    running = True
    while running:
        display_menu()
        
        try:
            choice = input("\nVotre choix: ").strip()
        except:
            print("\nAu revoir!")
            break
        
        if choice == "1":
            handle_balance_inquiry(data, accounts)
        elif choice == "2":
            t.display_all_transactions()
        elif choice == "3":
            print("\n--- Transactions par compte ---")
            print("Comptes disponibles:")
            for account in accounts:
                print(f"  - {account}")
            
            account_input = input("\nEntrez le nom du compte: ").strip()
            
            if account_input:
                validated_account = ac.validate_account_name(account_input)
                if validated_account:
                    t.display_transactions_by_account(validated_account)
                else:
                    print(f"Compte '{account_input}' introuvable!")
            else:
                print("Nom de compte invalide!")
        elif choice == "4":
            display_summary(data)
        elif choice == "5":
            handle_statistics(data)
        elif choice == "6":
            handle_export(data, accounts)
        elif choice == "7":
            handle_date_search(data)
        elif choice == "0":
            print("\nMerci d'avoir utilisé le système de gestion comptable!")
            print("Au revoir!")
            running = False
        else:
            print("❌ Choix invalide! Veuillez sélectionner une option valide.")
        
        if running and choice != "0":
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()