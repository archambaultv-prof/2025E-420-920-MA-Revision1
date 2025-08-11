# Calcule le solde d'un compte
def calculate_balance(data, account_name):
    balance = 0.0
    i = 0
    while i < len(data):
        transaction = data[i]
        if transaction['compte'] == account_name:
            balance += transaction['montant']
        i += 1
    return balance

# Retourne la liste des comptes uniques
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

# Verifie si le nom du compte existe
def validate_account_name(accounts, account_name):
    i = 0
    while i < len(accounts):
        if accounts[i].lower() == account_name.lower():
            return accounts[i]
        i += 1
    return None

# Affiche le solde de chaque compte
def display_summary(data):
    print("\n=== RÉSUMÉ DES COMPTES ===")
    accounts = get_all_accounts(data)
    i = 0
    while i < len(accounts):
        account = accounts[i]
        balance = calculate_balance(data, account)
        print(f"{account}: {balance:.2f}$")
        i += 1