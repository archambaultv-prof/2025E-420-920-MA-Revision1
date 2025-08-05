from typing import List
from datetime import datetime
import csv
from piledger.models.transaction import Transaction


def get_transactions_by_date_range(data, start_date, end_date):
    filtered_transactions = []
    i = 0
    while i < len(data):
        transaction = data[i]
        if start_date <= transaction['date'] <= end_date:
            filtered_transactions.append(transaction)
        i += 1
    return filtered_transactions

def find_largest_expense(data):
    largest_expense = None
    max_amount = 0
    i = 0
    while i < len(data):
        transaction = data[i]
        if transaction['montant'] > max_amount and transaction['compte'] != 'Compte courant' and transaction['compte'] != 'Revenu':
            max_amount = transaction['montant']
            largest_expense = transaction
        i += 1
    return largest_expense

def find_total_income(data):
    total = 0
    i = 0
    while i < len(data):
        transaction = data[i]
        if transaction['compte'] == 'Revenu':
            total += abs(transaction['montant'])
        i += 1
    return total

def find_total_expenses(data):
    total = 0
    i = 0
    while i < len(data):
        transaction = data[i]
        if transaction['compte'] != 'Compte courant' and transaction['compte'] != 'Revenu' and transaction['montant'] > 0:
            total += transaction['montant']
        i += 1
    return total

def export_account_postings(data, account_name, filename):
    file = open(filename, 'w', encoding='utf-8')
    file.write("No txn,Date,Compte,Montant,Commentaire\n")
    i = 0
    while i < len(data):
        transaction = data[i]
        if transaction['compte'] == account_name:
            line = f"{transaction['no_txn']},{transaction['date']},{transaction['compte']},{transaction['montant']},{transaction['commentaire']}\n"
            file.write(line)
        i += 1
    file.close()
    print(f"Écritures exportées vers {filename}")