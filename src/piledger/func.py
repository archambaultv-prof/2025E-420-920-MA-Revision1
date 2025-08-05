from .account import Account
from .transaction import Transaction
import csv


def read_data_file():  # Lire et analyser le fichier data.csv
    data = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            if len(row) >= 5:
                txn = Transaction(
                    no_txn=int(row[0]),
                    date=row[1],
                    account=Account(row[2]),
                    amount=float(row[3]),
                    comment=row[4]
                )
                data.append(txn)
    return data

def calculate_balance(data, account_name):  # Calculer le solde d'un compte
    balance = 0.0
    for transaction in data:
        if transaction.account.name == account_name:
            balance += transaction.amount
    return balance

def get_all_accounts(data):  # Extraire tous les noms de comptes uniques
    accounts = []
    for transaction in data:
        account = transaction.account
        if not any(acc.name == account.name for acc in accounts):
            accounts.append(account)
    return [acc.name for acc in accounts]

def get_transactions_by_date_range(data, start_date, end_date): # Filtrer les transactions par plage de dates
    filtered_transactions = []
    for transaction in data:
        if start_date <= transaction.date <= end_date:
            filtered_transactions.append(transaction)
    return filtered_transactions

def find_largest_expense(data): # Plus grosse dépense (hors compte courant et revenu)
    largest_expense = None
    max_amount = 0
    for transaction in data:
        if (transaction.amount > max_amount and 
            transaction.account.name != 'Compte courant' and 
            transaction.account.name != 'Revenu'):
            max_amount = transaction.amount
            largest_expense = transaction
    return largest_expense

def find_total_income(data): # Revenus totaux
    total = 0
    for transaction in data:
        if transaction.account.name == 'Revenu':
            total += abs(transaction.amount)
    return total

def find_total_expenses(data): # Dépenses totales (hors compte courant et revenu)
    total = 0
    for transaction in data:
        if (transaction.account.name != 'Compte courant' and 
            transaction.account.name != 'Revenu' and 
            transaction.amount > 0):
            total += transaction.amount
    return total

def export_account_postings(data, account_name, filename): # Exporter les écritures d'un compte vers un fichier CSV
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["No txn", "Date", "Compte", "Montant", "Commentaire"])
        for transaction in data:
            if transaction.account.name == account_name:
                csv_writer.writerow([
                    transaction.no_txn,
                    transaction.date,
                    transaction.account.name,
                    transaction.amount,
                    transaction.comment
                ])
    print(f"Écritures exportées vers {filename}")

def validate_account_name(accounts, account_name): # Validation du nom de compte (insensible à la casse)
    for account in accounts:
        if account.lower() == account_name.lower():
            return account
    return None

