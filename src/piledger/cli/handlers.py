from piledger.services.account_utils import calculate_balance, validate_account_name, get_all_accounts
from piledger.services.reports_utils import (
    find_total_income, find_total_expenses,
    find_largest_expense, export_account_postings,
    get_transactions_by_date_range
)

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

        
def display_all_transactions(data):
    print("\n=== TOUTES LES TRANSACTIONS ===")
    i = 0
    while i < len(data):
        transaction = data[i]
        print(f"Transaction {transaction['no_txn']} - {transaction['date']}")
        print(f"  Compte: {transaction['compte']}")
        print(f"  Montant: {transaction['montant']:.2f}$")
        if transaction['commentaire']:
            print(f"  Commentaire: {transaction['commentaire']}")
        print()
        i += 1

def display_transactions_by_account(data, account_name):
    print(f"\n=== TRANSACTIONS POUR LE COMPTE '{account_name}' ===")
    found_any = False
    i = 0
    while i < len(data):
        transaction = data[i]
        if transaction['compte'] == account_name:
            found_any = True
            print(f"Transaction {transaction['no_txn']} - {transaction['date']}")
            print(f"  Montant: {transaction['montant']:.2f}$")
            if transaction['commentaire']:
                print(f"  Commentaire: {transaction['commentaire']}")
            print()
        i += 1
    
    if not found_any:
        print(f"Aucune transaction trouvée pour le compte '{account_name}'")

def display_summary(data):
    print("\n=== RÉSUMÉ DES COMPTES ===")
    accounts = get_all_accounts(data)
    i = 0
    while i < len(accounts):
        account = accounts[i]
        balance = calculate_balance(data, account)
        print(f"{account}: {balance:.2f}$")
        i += 1
