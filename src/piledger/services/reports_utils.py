from typing import List
from datetime import datetime
import csv
from piledger.models.transaction import Transaction


def get_transactions_by_date_range(transaction: List[Transaction], start_date: str, end_date: str) -> List[Transaction]:
    """    Filtre les transactions dans une période donnée.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Format de date invalide. Utilisez YYYY-MM-DD.")
    return [
        txn for txn in transaction if start <= txn.date <= end
    ]   

def find_largest_expense(transactions: List[Transaction]) -> Transaction | None:
    """    Trouve la plus grande dépense dans les transactions.
    """
    if not transactions:
        return None   # Pas de transaction → pas de dépense
    largest_expense = None
    max_amount = 0
    for txn in transactions:
        if txn.montant < 0 and abs(txn.montant) > max_amount: 
            max_amount = abs(txn.montant) 
            largest_expense = txn
    return largest_expense


def find_total_income(transactions: List[Transaction]) -> float:
    """    Calcule le total des revenus à partir des transactions.
    """
    total = 0   
    for txn in transactions:
        # On suppose que les revenus sont toujours positifs
        if txn.compte.lower() == 'revenu' and txn.montant > 0:
            total += txn.montant
    return total


def find_total_expenses(transactions: List[Transaction]) -> float:
    """    Calcule le total des dépenses à partir des transactions.
    """
    total = 0   
    for txn in transactions:
        # On suppose que les dépenses sont toujours négatives
        # Vérifie que ce n’est pas un transfert ou un revenu
        if txn.compte.lower() not in ['revenu' , 'compte courant']and txn.montant < 0:
            total += abs(txn.montant)
    return total

def export_account_postings(transaction: List[Transaction], account_name: str, filename: str) -> None:
    """
    Exporte les écritures d'un compte spécifique vers un fichier CSV.
    """
    try:
     with open(filename, 'w',newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Écrit l’en-tête du fichier CSV
        writer.writerow(["No txn", "Date", "Compte", "Montant", "Commentaire"])
        for txn in transaction:
            if txn.compte.lower() == account_name.lower():
                writer.writerow([txn.no_txn, txn.date.strftime("%Y-%m-%d"), txn.compte, f"{txn.montant:.2f}", txn.commentaire]) 
        # Message de confirmation si tout s’est bien passé
        print(f"Écritures exportées vers {filename}")
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier {filename}: {e}")

         