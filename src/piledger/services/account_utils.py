from typing import List
from piledger.models.transaction import Transaction

def calculate_balance(transaction: List[Transaction], account_name: str) -> float:
    """
    Calcule le solde d'un compte spécifique à partir des transactions.
    """
    if not transaction:
        return 0.0
    if not account_name:
        raise ValueError("Le nom du compte ne peut pas être vide.")
    # On filtre les transactions correspondant au compte et on additionne les montants
    return sum(
        txn.montant for txn in transaction if txn.compte.lower() == account_name.lower()
    )
    

def get_all_accounts(transaction: List[Transaction]) -> List[str]:
    """
    Récupère tous les comptes uniques à partir des transactions.
    """
    accounts = set()
    for txn in transaction:
        accounts.add(txn.compte.lower())
    return list(accounts)


def validate_account_name(accounts: List[str], account_name: str) -> str:
    """
    Valide si le nom du compte existe dans la liste des comptes.
    """
    if not accounts:
        raise ValueError("La liste des comptes ne peut pas être vide.")
    if not account_name:
        raise ValueError("Le nom du compte ne peut pas être vide.")
    # On vérifie si le compte existe dans la liste
    for acc in accounts:
        if acc.lower() == account_name.lower():
            return acc
    return None   
