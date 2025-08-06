from typing import List
from piledger.models.transaction import Transaction
from piledger.services.account_utils import calculate_balance, validate_account_name, get_all_accounts
from piledger.services.reports_utils import (
    find_total_income, find_total_expenses,
    find_largest_expense, export_account_postings,
    get_transactions_by_date_range
)

def handle_balance_inquiry(transaction: list[Transaction], accounts: List[str]):
    """    Gère la consultation de solde pour un compte spécifique.
    """
    print("\n--- Consultation de solde ---")
    print("Comptes disponibles:")
    for acc in accounts:
        print(f" - {acc}")
    account_input = input("\nEntrez le nom du compte: ").strip()
    if not account_input:
        print("Nom de compte invalide!")
        return
    
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        balance = calculate_balance(transaction, validated_account)
        print(f"\nSolde du compte '{validated_account}': {balance:.2f}$")
        
    else:
        print(f"Compte '{account_input}' introuvable!")
        print("Vérifiez l'orthographe ou choisissez un compte dans la liste.")

def handle_statistics(transaction: List[Transaction]):
    """    Affiche des statistiques financières basées sur les transactions.
    """
    print("\n=== STATISTIQUES FINANCIÈRES ===")
    
    total_income = find_total_income(transaction)
    total_expenses = find_total_expenses(transaction)
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
    
    largest_expense = find_largest_expense(transaction)
    if largest_expense:
        print(f"\nPlus grosse dépense: {largest_expense['montant']:.2f}$ ({largest_expense['compte']})")
        if largest_expense['commentaire']:
            print(f"Commentaire: {largest_expense['commentaire']}")
    
    current_account_balance = calculate_balance(transaction, 'Compte courant')
    print(f"\nSolde du compte courant: {current_account_balance:.2f}$")

def handle_date_search(transaction: List[Transaction]):
    """    Gère la recherche de transactions dans une période donnée.
    """
    print("\n--- Recherche par période ---")
    start_date = input("Date de début (YYYY-MM-DD): ").strip()
    end_date = input("Date de fin (YYYY-MM-DD): ").strip()
    
    if not start_date or not end_date:
        print("Dates invalides!")
        return
    
    filtered_data = get_transactions_by_date_range(transaction, start_date, end_date)
    
    if len(filtered_data) == 0:
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:")
        for txn in filtered_data:
            print(txn)
            print()
            

def handle_export(transaction: List[Transaction], accounts: List[str]):
    """    Gère l'exportation des écritures d'un compte spécifique vers un fichier CSV.
    """
    print("\n--- Exportation ---")
    print("Comptes disponibles:")
    for acc in accounts:
        print(f" - {acc}")
    
    account_input = input("\nEntrez le nom du compte à exporter: ").strip()
    
    if not account_input:
        print("Nom de compte invalide!")
        return
    
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
        if not filename:
            filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
        
        export_account_postings(transaction, validated_account, filename)
    else:
        print(f"Compte '{account_input}' introuvable!")

        
def display_all_transactions(transaction: List[Transaction]):
    """    Affiche toutes les transactions.
    """
    print("\n=== TOUTES LES TRANSACTIONS ===")
    for txn in transaction:
        print(txn)
        print()
       

def display_transactions_by_account(transaction: List[Transaction], accounts: List[str]):
    """    Affiche les transactions pour un compte spécifique.
    """
    print(f"\n=== TRANSACTIONS POUR LE COMPTE  ===")
    for acc in accounts:
        print(f" -{acc}")    
    account_input = input("\nEntrez le nom du compte: ").strip()
    if not account_input:
        print("Nom de compte invalide!")
        return  
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        print(f"\nTransactions pour le compte '{validated_account}':")
        for txn in transaction:
            if txn.compte.lower() == validated_account.lower():
                print(txn)
                print()
    else:
        print(f"Compte '{account_input}' introuvable!")
        print("Vérifiez l'orthographe ou choisissez un compte dans la liste.")

def display_summary(transaction: List[Transaction]):
    """    Affiche un résumé des comptes et de leurs soldes.
    """
    print("\n=== RÉSUMÉ DES COMPTES ===")
    accounts = get_all_accounts(transaction)
    for acc in accounts:
        balance = calculate_balance(transaction, acc)
        print(f"Compte: {acc}, Solde: {balance:.2f}$")

