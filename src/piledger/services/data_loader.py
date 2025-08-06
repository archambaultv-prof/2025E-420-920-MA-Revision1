from typing import List
import csv
from piledger.models.transaction import Transaction


def read_data_file() -> List[Transaction]:
    """
    Lit les données depuis un fichier CSV et retourne une liste d'objets Transaction.
    """
    data = []

    try:
        with open('data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  

            for row in reader:
                try:
                    # Création d'une transaction avec validation
                    txn = Transaction(
                        no_txn=int(row['No txn']),
                        date=row['Date'],
                        compte=row['Compte'],
                        montant=float(row['Montant']),
                        commentaire=row.get('Commentaire', '')
                    )
                    data.append(txn)
                except ValueError as e:
                    print(f"ERREUR: {e} dans la ligne: {row}")
    except FileNotFoundError:
        print("ERREUR: Le fichier data.csv est introuvable!")

    return data

# def read_data_file():
#     data = []
#     with open('data.csv', 'r', encoding='utf-8') as file:
#      lines = file.readlines()

#     i = 0
#     while i < len(lines):
#         if i == 0:
#             i += 1
#             continue
#         line = lines[i].strip()
#         if line:
#             parts = []
#             current_part = ""
#             in_quotes = False
#             j = 0
#             while j < len(line):
#                 char = line[j]
#                 if char == '"':
#                     in_quotes = not in_quotes
#                 elif char == ',' and not in_quotes:
#                     parts.append(current_part)
#                     current_part = ""
#                     j += 1
#                     continue
#                 current_part += char
#                 j += 1
#             parts.append(current_part)
            
#             if len(parts) >= 5:
#                 try:
#                     txn = Transaction(
#                         no_txn=int(parts['No txn']),
#                         date=parts['Date'],
#                         compte=parts['Compte'],
#                         montant=float(parts['Montant']),
#                         commentaire=parts.get('Commentaire', '')
#                     )
#                     data.append(txn)
#                 except ValueError as e:
#                     print(f"ERREUR: {e} dans la ligne: {parts}")    
#         i += 1
    
#     return data