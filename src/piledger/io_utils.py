import csv
from piledger.transaction import Transaction

class CSVError(Exception):
    """Exception personnalisée pour les erreurs de lecture/écriture CSV."""
    pass


def read_data_file(filename: str) -> list[Transaction]:
    """
    Lit un fichier CSV et retourne une liste de Transaction.

    Args:
        filename (str): Chemin du fichier CSV.

    Returns:
        list[Transaction]: Liste des transactions lues.

    Raises:
        CSVError: Si le fichier est introuvable ou corrompu.
    """
    transactions: list[Transaction] = []

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Vérifier que les colonnes attendues existent
            expected_fields = {"Date", "Compte", "Montant", "Commentaire"}
            if not expected_fields.issubset(reader.fieldnames or []):
                raise CSVError(
                    f"Le fichier CSV doit contenir les colonnes : {', '.join(expected_fields)}"
                )

            for row in reader:
                try:
                    transactions.append(
                        Transaction(
                            date=row["Date"],
                            compte=row["Compte"],
                            montant=float(row["Montant"]),
                            commentaire=row.get("Commentaire", "")
                        )
                    )
                except ValueError as ve:
                    raise CSVError(f"Erreur de conversion des données : {ve}")

    except FileNotFoundError:
        raise CSVError(f"Fichier introuvable : {filename}")
    except Exception as e:
        raise CSVError(f"Erreur lors de la lecture du fichier {filename} : {e}")

    return transactions


def export_account_postings(filename: str, postings: list[Transaction]) -> None:
    """
    Exporte une liste de transactions dans un fichier CSV.

    Args:
        filename (str): Nom du fichier CSV à créer.
        postings (list[Transaction]): Liste des transactions à exporter.

    Raises:
        CSVError: Si l'export échoue.
    """
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Date", "Compte", "Montant", "Commentaire"]
            )
            writer.writeheader()
            for txn in postings:
                writer.writerow(txn.to_dict())
    except Exception as e:
        raise CSVError(f"Erreur lors de l'export vers {filename} : {e}")
