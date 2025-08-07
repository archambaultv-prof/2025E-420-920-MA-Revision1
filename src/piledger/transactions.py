class Transaction:
    def __init__(self, data):
        self.data = data

    def display_all_transactions(self):
        print("\n=== TOUTES LES TRANSACTIONS ===")
        for transaction in self.data:
            print(f"Transaction {transaction['no_txn']} - {transaction['date']}")
            print(f"  Compte: {transaction['compte']}")
            print(f"  Montant: {transaction['montant']:.2f}$")
            if transaction['commentaire']:
                print(f"  Commentaire: {transaction['commentaire']}")
            print()

    def display_transactions_by_account(self, account_name):
        print(f"\n=== TRANSACTIONS POUR LE COMPTE '{account_name}' ===")
        found_any = False
        for transaction in self.data:
            if transaction['compte'] == account_name:
                found_any = True
                print(f"Transaction {transaction['no_txn']} - {transaction['date']}")
                print(f"  Montant: {transaction['montant']:.2f}$")
                if transaction['commentaire']:
                    print(f"  Commentaire: {transaction['commentaire']}")
                print()
        
        if not found_any:
            print(f"Aucune transaction trouvée pour le compte '{account_name}'")

    def get_transactions_by_date_range(self, start_date, end_date):
        filtered_transactions = []
        for transaction in self.data:
            if start_date <= transaction['date'] <= end_date:
                filtered_transactions.append(transaction)
        return filtered_transactions