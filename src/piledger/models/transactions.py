class Transaction:
    """
    Représente une transaction financière avec un numéro, une date, un compte, un montant et un commentaire.
    """

    def __init__(self, no_txn, date, compte, montant, commentaire):
        self.no_txn = no_txn
        self.date = date
        self.compte = compte
        self.montant = montant
        self.commentaire = commentaire

    @classmethod
    def from_csv_line(cls, line: str):
        """
        Crée une instance de Transaction à partir d'une ligne CSV brute.

        Cette méthode gère les cas où certaines valeurs sont entourées de guillemets
        et contient des virgules. Elle divise manuellement la ligne CSV tout en respectant
        les valeurs entre guillemets.

        :param line: Ligne CSV à analyser.
        :return: Instance de Transaction.
        :raises ValueError: Si la ligne ne contient pas exactement 5 champs.
        """
        parts = []
        current_part = ''
        in_quotes = False

        for char in line:
            if char == '"':
                in_quotes = not in_quotes  # Gérer ouverture/fermeture des guillemets
            elif char == ',' and not in_quotes:
                parts.append(current_part.strip('"'))
                current_part = ''
                continue
            current_part += char

        parts.append(current_part.strip('"'))

        if len(parts) != 5:
            raise ValueError("CSV line must contain exactly 5 parts")

        return cls(
            no_txn=int(parts[0]),
            date=parts[1],
            compte=parts[2],
            montant=float(parts[3]),
            commentaire=parts[4]
        )

    def to_csv_line(self):
        """
        Convertit l'objet Transaction en une ligne CSV, avec des valeurs entourées de guillemets.

        :return: Ligne CSV (str)
        """
        return f'"{self.no_txn}","{self.date}","{self.compte}","{self.montant}","{self.commentaire}"'

    def __repr__(self):
        """
        Représentation lisible pour le débogage et l'affichage dans la console.

        :return: Représentation textuelle de l'objet Transaction.
        """
        return (
            f"Transaction(no_txn={self.no_txn}, date='{self.date}', "
            f"compte='{self.compte}', montant={self.montant}, commentaire='{self.commentaire}')"
        )
