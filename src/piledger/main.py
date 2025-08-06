import os
import csv
# from piledger.models import transaction
# from piledger.models.transaction import Transaction 
from piledger.services.data_loader import read_data_file
from piledger.services.account_utils import get_all_accounts, validate_account_name
from piledger.cli.menu import display_menu
from piledger.cli.handlers import (
    handle_balance_inquiry,
    display_all_transactions,
    display_transactions_by_account,
    display_summary,
    handle_statistics,
    handle_export,
    handle_date_search
)


def main():
    print("Chargement des données...")
    
    if not os.path.exists('data.csv'):
        print("ERREUR: Le fichier data.csv est introuvable!")
        print("Assurez-vous que le fichier se trouve à la racine du répertoire.")
        return
    
    transaction = read_data_file() #Lecture du fichier CSV 
    
    if not transaction:
        print("ERREUR: Aucune donnée n'a pu être chargée!")
        return
    
    print(f"✅ {len(transaction)} transactions chargées avec succès!")
    
    accounts = get_all_accounts(transaction)  # Récupération de tous les comptes uniques
    
    running = True
    while running:
        display_menu()
        
        try:
            choice = input("\nVotre choix: ").strip()
        except:
            print("\nAu revoir!")
            break

         # Gestion des choix
        if choice == "1":
            handle_balance_inquiry(transaction, accounts)
        elif choice == "2":
            display_all_transactions(transaction)
            
        elif choice == "3":
            print("\n--- Transactions par compte ---")
            print("Comptes disponibles:")
            
            for acc in accounts:
                print(f" - {acc}")
            
            account_input = input("\nEntrez le nom du compte: ").strip()
            
            if account_input:
                validated_account = validate_account_name(accounts, account_input)
                if validated_account:
                    display_transactions_by_account(transaction, validated_account)
                else:
                    print(f"Compte '{account_input}' introuvable!")
            else:
                print("Nom de compte invalide!")

        elif choice == "4":
            display_summary(transaction)
        elif choice == "5":
            handle_statistics(transaction)
        elif choice == "6":
            handle_export(transaction, accounts)
        elif choice == "7":
            handle_date_search(transaction)
        elif choice == "0":
            print("\nMerci d'avoir utilisé le système de gestion comptable!")
            print("Au revoir!")
            running = False
        else:
            print("❌ Choix invalide! Veuillez sélectionner une option valide.")
        
        if running and choice != "0":
            input("\nAppuyez sur Entrée pour continuer...")

# if __name__ == "__main__":
#     main()