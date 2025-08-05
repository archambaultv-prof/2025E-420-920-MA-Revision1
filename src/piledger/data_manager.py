# ===== data_manager.py =====
"""
Module pour la gestion des données (lecture/écriture de fichiers CSV).
"""

import csv
import os
from typing import List, Optional
from .models import Transaction
from .exceptions import FileError, DataValidationError


class CSVDataManager:
    """
    Gestionnaire pour la lecture et l'écriture de fichiers CSV.
    """
    
    def __init__(self, filename: str = 'data.csv'):
        """
        Initialise le gestionnaire de données.
        
        Args:
            filename: Nom du fichier CSV
        """
        self.filename = filename
    
    def load_transactions(self) -> List[Transaction]:
        """
        Charge les transactions depuis le fichier CSV.
        
        Returns:
            Liste des transactions chargées
            
        Raises:
            FileError: Si le fichier n'existe pas ou ne peut pas être lu
            DataValidationError: Si les données sont invalides
        """
        if not os.path.exists(self.filename):
            raise FileError(f"Le fichier '{self.filename}' n'existe pas")
        
        transactions = []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        transaction = Transaction(
                            no_txn=int(row['no_txn']),
                            date=row['date'].strip(),
                            compte=row['compte'].strip(),
                            montant=float(row['montant']),
                            commentaire=row.get('commentaire', '').strip()
                        )
                        transactions.append(transaction)
                        
                    except (ValueError, KeyError) as e:
                        raise DataValidationError(
                            f"Erreur ligne {row_num}: {e}"
                        ) from e
                        
        except IOError as e:
            raise FileError(f"Impossible de lire le fichier: {e}") from e
        
        return transactions
    
    def export_transactions(self, transactions: List[Transaction], 
                          filename: str) -> None:
        """
        Exporte les transactions vers un fichier CSV.
        
        Args:
            transactions: Liste des transactions à exporter
            filename: Nom du fichier de destination
            
        Raises:
            FileError: Si l'écriture échoue
        """
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['no_txn', 'date', 'compte', 'montant', 'commentaire']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for transaction in transactions:
                    writer.writerow({
                        'no_txn': transaction.no_txn,
                        'date': transaction.date,
                        'compte': transaction.compte,
                        'montant': transaction.montant,
                        'commentaire': transaction.commentaire
                    })
                    
        except IOError as e:
            raise FileError(f"Impossible d'écrire dans le fichier: {e}") from e