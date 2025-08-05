



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

def get_transactions_by_date_range(data, start_date, end_date):
    filtered_transactions = []
    i = 0
    while i < len(data):
        transaction = data[i]
        if start_date <= transaction['date'] <= end_date:
            filtered_transactions.append(transaction)
        i += 1
    return filtered_transactions