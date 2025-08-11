# Fonction lecture de donnees
def read_data_file():
    data = []
    file = open('data.csv', 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()
    
    i = 0
    while i < len(lines):
        if i == 0:
            i += 1
            continue
        line = lines[i].strip()
        if line:
            parts = []
            current_part = ""
            in_quotes = False
            j = 0
            while j < len(line):
                char = line[j]
                if char == '"':
                    in_quotes = not in_quotes
                elif char == ',' and not in_quotes:
                    parts.append(current_part)
                    current_part = ""
                    j += 1
                    continue
                current_part += char
                j += 1
            parts.append(current_part)
            
            if len(parts) >= 5:
                txn_dict = {}
                txn_dict['no_txn'] = int(parts[0])
                txn_dict['date'] = parts[1]
                txn_dict['compte'] = parts[2]
                txn_dict['montant'] = float(parts[3])
                txn_dict['commentaire'] = parts[4]
                data.append(txn_dict)
        i += 1
    
    return data

# Fonction ecriture de donnees
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