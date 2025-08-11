from piledger.io_utils import CSVError, read_data_file, export_account_postings
from piledger.ledger import Ledger
from piledger.transaction import Transaction

DATA_FILE = "data.csv"

def main() -> None:
    ledger = Ledger()

    try:
        transactions = read_data_file(DATA_FILE)
        for txn in transactions:
            ledger.add_transaction(txn)
    except CSVError as e:
        print(f"Erreur: {e}")
        return

    print("📒 Comptes disponibles :", ", ".join(ledger.list_accounts()))

    compte = input("Entrez le nom du compte pour voir ses écritures : ").strip()
    postings = ledger.filter_by_account(compte)

    if not postings:
        print(f"Aucune écriture trouvée pour le compte '{compte}'.")
        return

    for txn in postings:
        print(txn)

    print(f"💰 Solde du compte '{compte}' : {ledger.get_balance(compte):.2f} $")

    if input("Voulez-vous ajouter une transaction ? (o/n) ").lower() == "o":
        date = input("Date (YYYY-MM-DD) : ")
        compte_txn = input("Compte : ")
        montant = float(input("Montant : "))
        commentaire = input("Commentaire : ")

        ledger.add_transaction(Transaction(date, compte_txn, montant, commentaire))
        print("✅ Transaction ajoutée et enregistrée.")

    # Nouveau bloc : Export CSV
    if input("Exporter les écritures de ce compte ? (o/n) ").lower() == "o":
        filename = input("Nom du fichier CSV (ex: export.csv) : ")
        try:
            export_account_postings(filename, postings)
            print(f"💾 Écritures exportées dans '{filename}'")
        except CSVError as e:
            print(f"Erreur export : {e}")

if __name__ == "__main__":
    main()
