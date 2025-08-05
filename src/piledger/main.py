from .func import get_all_accounts, read_data_file
from .main_menu import display_menu
import os





def main():
    print("Chargement des données...")
    
    if not os.path.exists('data.csv'):
        raise FileNotFoundError("ERREUR: Le fichier data.csv est introuvable!")
        print("Assurez-vous que le fichier se trouve à la racine du répertoire.")
        return
    
    data = read_data_file()
    
    if len(data) == 0:
        raise ValueError("ERREUR: Aucune donnée n'a pu être chargée!")
        return
    
    print(f"✅ {len(data)} transactions chargées avec succès!")
    
    accounts = get_all_accounts(data)
    
    running = True
    while running:
        running = display_menu(data, accounts)
        
        

if __name__ == "__main__":
    main()