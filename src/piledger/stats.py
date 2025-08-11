# Trouve la plus grosse depense (hors compte courant et revenu)
def find_largest_expense(data):
    largest_expense = None
    max_amount = 0
    for transaction in data:
        if transaction['montant'] > max_amount and transaction['compte'] != 'Compte courant' and transaction['compte'] != 'Revenu':
            max_amount = transaction['montant']
            largest_expense = transaction
    return largest_expense

# Calcule le total des revenus
def find_total_income(data):
    total = 0
    for transaction in data:
        if transaction['compte'] == 'Revenu':
            total += abs(transaction['montant'])
    return total

# Calcule le total des depenses (hors compte courant et revenu)
def find_total_expenses(data):
    total = 0
    for transaction in data:
        if transaction['compte'] != 'Compte courant' and transaction['compte'] != 'Revenu' and transaction['montant'] > 0:
            total += transaction['montant']
    return total