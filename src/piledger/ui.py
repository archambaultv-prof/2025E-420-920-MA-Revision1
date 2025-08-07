
from piledger.accounts import Account

def display_summary(data):
    print("\n=== RÉSUMÉ DES COMPTES ===")
    ac = Account(data)
    accounts = ac.get_all_accounts()
    for account in accounts:
        balance = ac.calculate_balance(account)
        print(f"{account}: {balance:.2f}$")


def display_menu():
    print("\n" + "="*50)
    print("SYSTÈME DE GESTION COMPTABLE PERSONNEL")
    print("="*50)
    print("1. Afficher le solde d'un compte")
    print("2. Afficher toutes les transactions")
    print("3. Afficher les transactions d'un compte")
    print("4. Afficher le résumé de tous les comptes")
    print("5. Afficher les statistiques")
    print("6. Exporter les écritures d'un compte")
    print("7. Rechercher par période")
    print("0. Quitter")
    print("="*50)
