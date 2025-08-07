import csv
from .models import Transaction
from pathlib import Path


class DataManager:
    @staticmethod
    def load_transactions(filename="data.csv"):
        """Charge les transactions depuis un fichier CSV avec chemin relatif sûr"""
        transactions = []
        
        # 1. Essayer le chemin du fichier exécutable
        base_path = Path(__file__).parent
        data_path = base_path / filename
        
        # 2. Essayer le chemin du working directory
        if not data_path.exists():
            data_path = Path(filename)
        
        try:
            with open(data_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transactions.append(Transaction(
                        row['No txn'],
                        row['Date'],
                        row['Compte'],
                        row['Montant'],
                        row['Commentaire']
                    ))
            print(f"✅ {len(transactions)} transactions chargées depuis {data_path}")
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé : {data_path.absolute()}")
        except Exception as e:
            print(f"❌ Erreur de lecture : {e}")
        
        return transactions

    @staticmethod
    def export_transactions(transactions, account_name, filename):
        """Exporte les transactions d'un compte vers un CSV."""
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['No txn', 'Date', 'Compte', 'Montant', 'Commentaire'])
            for t in transactions:
                if t.compte == account_name:
                    writer.writerow([t.no_txn, t.date, t.compte, t.montant, t.commentaire])
        print(f"➡ Export terminé dans {filename}")