

def calculate_balance(data, account_name):
    balance = 0.0
    for transaction in data:
        if transaction['compte'] == account_name:
            balance += transaction['montant']
    return balance

def get_all_accounts(data):
    accounts = []
    i = 0
    while i < len(data):
        transaction = data[i]
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

def validate_account_name(accounts, account_name):
    i = 0
    while i < len(accounts):
        if accounts[i].lower() == account_name.lower():
            return accounts[i]
        i += 1
    return None