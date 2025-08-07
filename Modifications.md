**Récapitulatif des modifications apportées**

### Point d'entrée:
- Simplification du point d'entrée: Suppression de l'importation de main dans lui-meme. La fonction main() est maintenant définie localement dans main.py ce qui évite toute récursion inutile. 
- Ajout de "piledger.main:main" dans le fichier pyproject.toml afin d’indiquer que l’exécution du programme doit appeler la fonction main() située dans le module main.py.
- Module __init__.py vide

### Lecture du fichier de données:
- Remplacer open et close dans read_data_file par with permettant la fermeture automatique du fichier meme en cas d'erreur
- Remplacement du traitement manuel des lignes CSV par l'utilisation du module csv.reader qui gère correctement les séparateurs, les guillemets et les champs multiples. Ce qui simplifie le code et améliore la compatibilité avec d'autres outils ce qui facilite la collaboration.

### Calcul du solde:
Simplification de la fonction calculate_balance en remplacant la boucle while manuelle par une boucle for plus lisible. Ce qui rend le code plus clair et réduit les risques d'erreurs liés à la gestion manuelle de l'indice.

### Séparation des fonctions par module:
- data_handler.py ayant comme thème l'import et l'export des données
- transaction.py pour toutes les fonctions en lien directe avec les transactions
- account.py pour les fonctionnalités liées au comptes

