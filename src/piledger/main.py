#    
#    ░█████████  ░██ ░██                   ░██                                
#    ░██     ░██     ░██                   ░██                                
#    ░██     ░██ ░██ ░██  ░███████   ░████████  ░████████  ░███████  ░██░████ 
#    ░█████████  ░██ ░██ ░██    ░██ ░██    ░██ ░██    ░██ ░██    ░██ ░███     
#    ░██         ░██ ░██ ░█████████ ░██    ░██ ░██    ░██ ░█████████ ░██      
#    ░██         ░██ ░██ ░██        ░██   ░███ ░██   ░███ ░██        ░██      
#    ░██         ░██ ░██  ░███████   ░█████░██  ░█████░██  ░███████  ░██      
#                                                     ░██                     
#                                                ░███████                      
#                                                                       

# Le programme ne fonctionne malheureusement pas.
# J’ai essayé de séparer les blocs de code en plusieurs fichiers mais le programme ne démarre plus :^)

import os
from .data import read_data_file, export_account_postings
from .accounts import calculate_balance, get_all_accounts, validate_account_name, display_summary
from .transactions import display_all_transactions, display_transactions_by_account, get_transactions_by_date_range
from .stats import find_largest_expense, find_total_income, find_total_expenses
from .ui import display_menu

# Gere la consultation du solde d'un compte
def handle_balance_inquiry(data, accounts):
    print("\n--- Consultation de solde ---")
    print("Comptes disponibles:")
    i = 0
    while i < len(accounts):
        print(f"  - {accounts[i]}")
        i += 1
    
    account_input = input("\nEntrez le nom du compte: ").strip()
    
    if not account_input:
        print("Nom de compte invalide!")
        return
    
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        balance = calculate_balance(data, validated_account)
        print(f"\nSolde du compte '{validated_account}': {balance:.2f}$")
        
    else:
        print(f"Compte '{account_input}' introuvable!")
        print("Vérifiez l'orthographe ou choisissez un compte dans la liste.")

# Affiche les statistiques financieres globales
def handle_statistics(data):
    print("\n=== STATISTIQUES FINANCIÈRES ===")
    
    total_income = find_total_income(data)
    total_expenses = find_total_expenses(data)
    net_worth = total_income - total_expenses
    
    print(f"Revenus totaux: {total_income:.2f}$")
    print(f"Dépenses totales: {total_expenses:.2f}$")
    print(f"Situation nette: {net_worth:.2f}$")
    
    if net_worth > 0:
        print("📈 Situation financière positive")
    elif net_worth < 0:
        print("📉 Situation financière négative")
    else:
        print("⚖️  Situation financière équilibrée")
    
    largest_expense = find_largest_expense(data)
    if largest_expense:
        print(f"\nPlus grosse dépense: {largest_expense['montant']:.2f}$ ({largest_expense['compte']})")
        if largest_expense['commentaire']:
            print(f"Commentaire: {largest_expense['commentaire']}")
    
    current_account_balance = calculate_balance(data, 'Compte courant')
    print(f"\nSolde du compte courant: {current_account_balance:.2f}$")

# Permet la recherche et l'affichage des transactions sur une periode donnee
def handle_date_search(data):
    print("\n--- Recherche par période ---")
    start_date = input("Date de début (YYYY-MM-DD): ").strip()
    end_date = input("Date de fin (YYYY-MM-DD): ").strip()
    
    if not start_date or not end_date:
        print("Dates invalides!")
        return
    
    filtered_data = get_transactions_by_date_range(data, start_date, end_date)
    
    if len(filtered_data) == 0:
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:")
        i = 0
        while i < len(filtered_data):
            transaction = filtered_data[i]
            print(f"  {transaction['date']} - {transaction['compte']}: {transaction['montant']:.2f}$")
            i += 1

# Gere l'exportation des transactions d'un compte vers un fichier CSV
def handle_export(data, accounts):
    print("\n--- Exportation ---")
    print("Comptes disponibles:")
    i = 0
    while i < len(accounts):
        print(f"  - {accounts[i]}")
        i += 1
    
    account_input = input("\nEntrez le nom du compte à exporter: ").strip()
    
    if not account_input:
        print("Nom de compte invalide!")
        return
    
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
        if not filename:
            filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
        
        export_account_postings(data, validated_account, filename)
    else:
        print(f"Compte '{account_input}' introuvable!")

# Fonction principale qui lance le programme et gere le menu principal
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
    
    accounts = get_all_accounts(data)
    
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
            display_all_transactions(data)
        elif choice == "3":
            print("\n--- Transactions par compte ---")
            print("Comptes disponibles:")
            i = 0
            while i < len(accounts):
                print(f"  - {accounts[i]}")
                i += 1
            
            account_input = input("\nEntrez le nom du compte: ").strip()
            
            if account_input:
                validated_account = validate_account_name(accounts, account_input)
                if validated_account:
                    display_transactions_by_account(data, validated_account)
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