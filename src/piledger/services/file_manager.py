import os
from ..models.transactions import Transaction

class FileManager:
    """
    Gère la lecture et l'écriture des transactions à partir d'un fichier CSV.
    """

    def __init__(self, file_path):
        """
        Initialise le gestionnaire de fichiers avec le chemin du fichier CSV à utiliser.
        :param file_path: Chemin vers le fichier contenant les transactions.
        """
        self.file_path = file_path

    def read_transactions(self):
        """
        Lit les transactions depuis le fichier CSV et retourne une liste d'objets Transaction.

        Cette méthode :
        - Ignore la première ligne (l'en-tête).
        - Ignore les lignes vides.
        - Gère les erreurs de format ligne par ligne (ex : mauvais nombre de colonnes).

        :return: Liste d'objets Transaction.
        """
        transactions = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines[1:]:  # Sauter l'en-tête
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        transaction = Transaction.from_csv_line(line)
                        transactions.append(transaction)
                    except ValueError as ve:
                        print(f"Erreur de format dans la ligne ignorée: {line} → {ve}")
        except FileNotFoundError:
            print(f"❌ Fichier '{self.file_path}' introuvable.")
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier: {e}")
        return transactions

    def export_transactions(self, transactions, filename):
        """
        Exporte une liste de transactions vers un fichier CSV.

        - Si le fichier n'existe pas, il est créé avec l'en-tête.
        - Si le fichier existe, les nouvelles transactions sont ajoutées à la suite.

        :param transactions: Liste d'objets Transaction à exporter.
        :param filename: Nom du fichier cible pour l’exportation.
        """
        # Si le fichier n'existe pas encore, on ajoute l'en-tête.
        write_header = not os.path.exists(filename)

        with open(filename, 'a', encoding='utf-8') as file:
            if write_header:
                file.write("No txn,Date,Compte,Montant,Commentaire\n")
            for txn in transactions:
                file.write(txn.to_csv_line() + "\n")

        print(f"✅ {len(transactions)} transactions ajoutées à {filename}")
