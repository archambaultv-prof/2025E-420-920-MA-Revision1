# Affiche le menu principal
def display_menu():
    print("\n" + "="*50)
    print("SYSTEME DE GESTION COMPTABLE PERSONNEL")
    print("="*50)
    print("1. Afficher le solde d'un compte")
    print("2. Afficher toutes les transactions")
    print("3. Afficher les transactions d'un compte")
    print("4. Afficher le resume de tous les comptes")
    print("5. Afficher les statistiques")
    print("6. Exporter les ecritures d'un compte")
    print("7. Rechercher par periode")
    print("0. Quitter")
    print("="*50)

# Affiche la liste des comptes disponibles
def display_accounts(accounts):
    print("Comptes disponibles:")
    for acc in accounts:
        print(f"  - {acc}")

# Affiche un message d'erreur simple
def display_error(msg):
    print(f"Erreur: {msg}")