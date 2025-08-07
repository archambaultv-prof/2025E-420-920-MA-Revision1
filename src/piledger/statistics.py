
from piledger.accounts import Account
from piledger.transactions import Transaction

def get_transaction_amount(transaction):
    return transaction['montant']

def find_largest_expense(data):
    expenses = [
        transaction
        for transaction in data
        if transaction['compte'] not in ('Compte courant', 'Revenu')
    ]
    largest_expense = max(expenses, key=get_transaction_amount, default=None)
    return largest_expense

def find_total_income(data):
    all_income = [
        abs(transaction['montant'])
        for transaction in data
        if transaction['compte'] == 'Revenu'
    ]
    total = sum(all_income)
    return total

def find_total_expenses(data):
    all_expenses = [
        transaction['montant']
        for transaction in data
        if transaction['compte'] not in ('Compte courant', 'Revenu') and transaction['montant'] > 0
    ]
    total = sum(all_expenses)
    return total


def handle_balance_inquiry(data, accounts):
    print("\n--- Consultation de solde ---")
    print("Comptes disponibles:")
    for account in accounts:
        print(f"  - {account}")
    
    account_input = input("\nEntrez le nom du compte: ").strip()
    
    if not account_input:
        print("Nom de compte invalide!")
        return
    ac = Account(data)
    validated_account = ac.validate_account_name(account_input)
    
    if validated_account:
        balance = ac.calculate_balance(validated_account)
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

    ac = Account(data)
    current_account_balance = ac.calculate_balance('Compte courant')
    print(f"\nSolde du compte courant: {current_account_balance:.2f}$")


def handle_date_search(data):
    print("\n--- Recherche par période ---")
    start_date = input("Date de début (YYYY-MM-DD): ").strip()
    end_date = input("Date de fin (YYYY-MM-DD): ").strip()
    
    if not start_date or not end_date:
        print("Dates invalides!")
        return
    
    t = Transaction(data)
    filtered_data = t.get_transactions_by_date_range(start_date, end_date)

   
    if len(filtered_data) == 0:
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:")
        for transaction in filtered_data:
            print(f"  {transaction['date']} - {transaction['compte']}: {transaction['montant']:.2f}$")
