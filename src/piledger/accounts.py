
class Account:
    def __init__(self, data):
        self.data = data
        self.accounts = self.get_all_accounts()

    def calculate_balance(self, account_name):
        balance = 0.0
        for transaction in self.data:
            if transaction['compte'] == account_name:
                balance += transaction['montant']
        return balance

    def get_all_accounts(self):
        accounts = []
        i = 0
        while i < len(self.data):
            transaction = self.data[i]
            account = transaction['compte']
            found = False
            j = 0
            while j < len(accounts):
                if accounts[j] == account:
                    found = True
                    break
                j += 1
            if not found:
                accounts.append(account)
            i += 1
        return accounts

    def validate_account_name(self, account_name):
        i = 0
        while i < len(self.accounts):
            if self.accounts[i].lower() == account_name.lower():
                return self.accounts[i]
            i += 1
        return None