import csv
from piledger.accounts import Account
def read_data_file():
    data = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 5:
                txn_dict = {
                    'no_txn': int(row[0]),
                    'date': row[1],
                    'compte': row[2],
                    'montant': float(row[3]),
                    'commentaire': row[4]
                }
                data.append(txn_dict)
    return data

def export_account_postings(data, account_name, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("No txn,Date,Compte,Montant,Commentaire\n")
        for transaction in data:
            if transaction['compte'] == account_name:
                line = f"{transaction['no_txn']},{transaction['date']},{transaction['compte']},{transaction['montant']},{transaction['commentaire']}\n"
                file.write(line)
    print(f"Écritures exportées vers {filename}")


def handle_export(data, accounts):
    print("\n--- Exportation ---")
    print("Comptes disponibles:")
    for account in accounts:
        print(f"  - {account}")
    
    account_input = input("\nEntrez le nom du compte à exporter: ").strip()
    
    if not account_input:
        print("Nom de compte invalide!")
        return
    ac = Account(data)
    validated_account = ac.validate_account_name(account_input)
    
    if validated_account:
        filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
        if not filename:
            filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
        
        export_account_postings(data, validated_account, filename)
    else:
        print(f"Compte '{account_input}' introuvable!")