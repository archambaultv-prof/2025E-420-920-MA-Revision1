# ===== exceptions.py =====
"""
Module contenant les exceptions personnalisees pour le systeme comptable.
"""
class ComptabiliteError(Exception):
    """Exception de base pour le système de comptabilité."""
    pass


class FileError(ComptabiliteError):
    """Exception levée lors d'erreurs de fichier."""
    pass


class DataValidationError(ComptabiliteError):
    """Exception levée lors d'erreurs de validation des données."""
    pass


class AccountNotFoundError(ComptabiliteError):
    """Exception levée quand un compte n'est pas trouvé."""
    pass