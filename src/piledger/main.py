# ===== main.py =====
"""
Point d'entrée principal de l'application.
"""
from .account_manager import AccountManager
from .data_manager import CSVDataManager
from .ui import UserInterface

def main() -> None:
    """Fonction principale de l'application."""
    data_manager = CSVDataManager('data.csv')
    account_manager = AccountManager([])  # Sera rechargé par l'UI
    ui = UserInterface(account_manager, data_manager)
    ui.run()


if __name__ == "__main__":
    main() 