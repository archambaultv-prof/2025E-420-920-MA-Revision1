import csv

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