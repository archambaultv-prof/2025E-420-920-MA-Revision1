from .func import (
    get_all_accounts, calculate_balance, read_data_file, validate_account_name,
    find_total_income, find_total_expenses, find_largest_expense, 
    export_account_postings, get_transactions_by_date_range
)

        
        
def display_menu(data, accounts):
    print("\n" + "="*50)
    print("SYSTÈME DE GESTION COMPTABLE PERSONNEL")
    print("="*50)
    print("1. Afficher le solde d'un compte")
    print("2. Afficher toutes les transactions")
    print("3. Afficher les transactions d'un compte")
    print("4. Afficher le résumé de tous les comptes")
    print("5. Afficher les statistiques")
    print("6. Exporter les écritures d'un compte")
    print("7. Rechercher par période")
    print("0. Quitter")
    print("="*50)

    try:
        choice = input("\nVotre choix: ").strip()
    except ValueError:
        print("❌ Entrée invalide! Veuillez entrer un nombre.")
        
            
    if choice == "1":
        handle_balance_inquiry(data, accounts)
    elif choice == "2":
        display_all_transactions(data)
    elif choice == "3":
        print("\n--- Transactions par compte ---")
        print("Comptes disponibles:")
        for account in accounts:
            print(f"  - {account}")
                
        account_input = input("\nEntrez le nom du compte: ").strip()
                
        if account_input:
            validated_account = validate_account_name(accounts, account_input)
            if validated_account:
                display_transactions_by_account(data, validated_account)
            else:
                raise ValueError(f"Compte '{account_input}' introuvable!")
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
        return False
    else:
        raise ValueError("❌ Choix invalide! Veuillez sélectionner une option valide.")
        
    if choice != "0":
        input("\nAppuyez sur Entrée pour continuer...")  #!!!!evaluer si meilleur option
    return True    

def handle_balance_inquiry(data, accounts):  # Choix 1
    print("\n--- Consultation de solde ---")
    print("Comptes disponibles:")
    for account in accounts:
        print(f"  - {account}")
    
    account_input = input("\nEntrez le nom du compte: ").strip()
    
    if not account_input:
        print("Nom de compte invalide!")
        return
    
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        balance = calculate_balance(data, validated_account)
        print(f"\nSolde du compte '{validated_account}': {balance:.2f}$")
        
    else:
        raise ValueError(f"Compte '{account_input}' introuvable!")
        print("Vérifiez l'orthographe ou choisissez un compte dans la liste.")

def display_all_transactions(data): # Choix 2
    print("\n=== TOUTES LES TRANSACTIONS ===")
    for transaction in data:
        print(f"Transaction {transaction.no_txn} - {transaction.date}")
        print(f"  Compte: {transaction.account.name}")
        print(f"  Montant: {transaction.amount:.2f}$")
        if transaction.comment:
            print(f"  Commentaire: {transaction.comment}")
        print()
        
def display_transactions_by_account(data, account_name): # Choix 3
    print(f"\n=== TRANSACTIONS POUR LE COMPTE '{account_name}' ===")
    found_any = False
    for transaction in data:
        if transaction.account.name == account_name:
            found_any = True
            print(f"Transaction {transaction.no_txn} - {transaction.date}")
            print(f"  Montant: {transaction.amount:.2f}$")
            if transaction.comment:
                print(f"  Commentaire: {transaction.comment}")
            print()
    
    if not found_any:
        raise ValueError(f"Aucune transaction trouvée pour le compte '{account_name}'")

def display_summary(data): # Choix 4
    print("\n=== RÉSUMÉ DES COMPTES ===")
    accounts = get_all_accounts(data)
    for account in accounts:
        balance = calculate_balance(data, account)
        print(f"{account}: {balance:.2f}$")        
        

def handle_statistics(data): # Choix 5
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
        print(f"\nPlus grosse dépense: {largest_expense.amount:.2f}$ ({largest_expense.account.name})")
        if largest_expense.comment:
            print(f"Commentaire: {largest_expense.comment}")
    
    current_account_balance = calculate_balance(data, 'Compte courant')
    print(f"\nSolde du compte courant: {current_account_balance:.2f}$")


def handle_export(data, accounts): # Choix 6
    print("\n--- Exportation ---")
    print("Comptes disponibles:")
    for account in accounts:
        print(f"  - {account}")
    
    account_input = input("\nEntrez le nom du compte à exporter: ").strip()
    
    if not account_input:
        raise ValueError("Nom de compte invalide!")
    
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
        if not filename:
            filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
        
        export_account_postings(data, validated_account, filename)
    else:
        raise ValueError(f"Compte '{account_input}' introuvable!")
        
def handle_date_search(data): # Choix 7
    print("\n--- Recherche par période ---")
    start_date = input("Date de début (YYYY-MM-DD): ").strip()
    end_date = input("Date de fin (YYYY-MM-DD): ").strip()
    
    if not start_date or not end_date:
        raise ValueError("Dates invalides!")
        return
    
    filtered_data = get_transactions_by_date_range(data, start_date, end_date)
    
    if len(filtered_data) == 0:
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:")
        for transaction in filtered_data:
            print(f"  {transaction.date} - {transaction.account.name}: {transaction.amount:.2f}$")

        