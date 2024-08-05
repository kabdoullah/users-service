from sqlalchemy.orm import Session
from app.models.data.user import User


def generate_reference(db: Session, prefix: str = "UT-PA") -> str:
    """
    Génère une référence unique au format UT-PA000001.

    :param db: Session SQLAlchemy
    :param prefix: Préfixe pour la référence (par défaut "UT-PA")
    :return: Référence unique
    """
    # Récupère la dernière référence existante dans la base de données
    last_user = db.query(User).order_by(User.reference.desc()).first()

    if last_user and last_user.reference:
        # Extrait le numéro de la dernière référence et l'incrémente
        last_number = int(last_user.reference[len(prefix):])
        new_number = last_number + 1
    else:
        new_number = 1

    # Génère la nouvelle référence en ajoutant des zéros pour respecter le format
    new_reference = f"{prefix}{new_number:06d}"
    return new_reference
