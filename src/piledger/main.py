from .services.file_manager import FileManager
from .services.transactions_service import TransactionService
from .services.menu import MenuHandler

"""
Point d'entrée principal de l'application PiLedger.

Ce module initialise les composants essentiels :
- FileManager pour lire et écrire les transactions.
- TransactionService pour exécuter la logique métier.
- MenuHandler pour gérer l'interaction avec l'utilisateur via le menu.

Il démarre une boucle interactive qui permet à l'utilisateur de naviguer dans les fonctionnalités du programme.
"""

def main():
    """
    Fonction principale qui initialise les services nécessaires et lance la boucle du menu utilisateur.
    Elle gère aussi les erreurs liées à une saisie invalide de l'utilisateur (ex: texte au lieu d’un chiffre).
    """
    
    file_path = "data.csv"  # Chemin vers le fichier contenant les transactions CSV

    # Initialisation des différents modules du programme :
    # - file_manager lit les données du fichier CSV,
    # - service applique les opérations sur ces données (solde, dépenses, etc.),
    # - menu orchestre l'interaction utilisateur.
    file_manager = FileManager(file_path)
    service = TransactionService(file_manager)
    menu = MenuHandler(service, file_manager)

    # Boucle principale du menu. Elle s'arrête uniquement lorsque l'utilisateur choisit l'option 8 (Quitter).
    while True:
        menu.display_menu()
        try:
            choice = int(input("Votre choix: "))
            if choice == 8:
                break  # Quitte la boucle si l'utilisateur veut sortir
            menu.handle_user_selection(choice)
        except ValueError:
            print("Veuillez entrer un chiffre valide.")  # Saisie non numérique


if __name__ == "__main__":
    main()
