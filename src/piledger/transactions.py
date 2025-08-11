# Affiche toutes les transactions
def display_all_transactions(data):
    print("\n=== Toutes les transactions ===")
    for transaction in data:
        print(f"Transaction {transaction['no_txn']} - {transaction['date']}")
        print(f"  Compte: {transaction['compte']}")
        print(f"  Montant: {transaction['montant']:.2f}$")
        if transaction['commentaire']:
            print(f"  Commentaire: {transaction['commentaire']}")
        print()

# Affiche les transactions d'un compte specifique
def display_transactions_by_account(data, account_name):
    print(f"\n=== Transactions pour le compte '{account_name}' ===")
    found_any = False
    for transaction in data:
        if transaction['compte'] == account_name:
            found_any = True
            print(f"Transaction {transaction['no_txn']} - {transaction['date']}")
            print(f"  Montant: {transaction['montant']:.2f}$")
            if transaction['commentaire']:
                print(f"  Commentaire: {transaction['commentaire']}")
            print()
    if not found_any:
        print(f"Aucune transaction trouvee pour le compte '{account_name}'")

# Retourne les transactions entre deux dates (YYYY-MM-DD)
def get_transactions_by_date_range(data, start_date, end_date):
    filtered_transactions = []
    for transaction in data:
        if start_date <= transaction['date'] <= end_date:
            filtered_transactions.append(transaction)
    return filtered_transactions